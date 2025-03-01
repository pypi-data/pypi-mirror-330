# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import heapq
import logging
import re
import uuid
from collections.abc import Iterator
from typing import cast

import attrs
import lance
import pyarrow as pa
import ray.actor
import ray.data
import ray.util.queue
from tqdm.auto import tqdm

from geneva.apply import LanceRecordBatchUDFApplier, ReadTask, plan_read
from geneva.checkpoint import CheckpointStore
from geneva.debug.logger import CheckpointStoreErrorLogger
from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)


def _combine_chunks(arr: pa.Array) -> pa.Array:
    if isinstance(arr, pa.ChunkedArray):
        assert len(arr.chunks) == 1
        return arr.chunks[0]
    return arr


@ray.remote
@attrs.define
class ApplierActor:
    applier: LanceRecordBatchUDFApplier

    def run(self, task) -> tuple[ReadTask, dict[str, str]]:
        return task, self.applier.run(task)


ApplierActor: ray.actor.ActorClass = cast(ray.actor.ActorClass, ApplierActor)


@ray.remote
@attrs.define
class FragmentWriter:
    uri: str
    column_name: str
    store: CheckpointStore

    fragment_id: int

    checkpoint_keys: ray.util.queue.Queue

    def write(self) -> tuple[int, lance.fragment.DataFile]:
        dataset = lance.dataset(self.uri)
        import more_itertools

        buffer: list[tuple[int, dict[str, str]]] = []
        num_rows = dataset.get_fragment(self.fragment_id).count_rows()
        written_rows = 0

        def _iter() -> Iterator[pa.RecordBatch]:
            nonlocal written_rows
            while written_rows < num_rows:
                while not buffer or buffer[0][0] != written_rows:
                    batch: tuple[int, dict[str, str]] = self.checkpoint_keys.get()
                    heapq.heappush(buffer, batch)

                data = heapq.heappop(buffer)[1]
                res = pa.RecordBatch.from_pydict(
                    {
                        key: _combine_chunks(self.store[value]["data"])
                        for key, value in data.items()
                    }
                )
                yield res
                written_rows += res.num_rows

        it = more_itertools.peekable(_iter())
        rbr = pa.RecordBatchReader.from_batches(it.peek().schema, it)

        # TODO: this doesn't support struct or complex schema yet
        new_data = lance.fragment.write_fragments(
            rbr,
            self.uri,
            max_rows_per_file=1 << 31,
            max_bytes_per_file=1 << 40,
        )

        assert len(new_data) == 1
        new_data = new_data[0]
        assert len(new_data.files) == 1
        new_datafile = new_data.files[0]

        # MASSIVE HACK: open up an API to get the field id from the column name
        field_id = re.compile(
            rf'name: "{self.column_name}", id: (?P<field_id>[\d]*),'
        ).findall(str(dataset.lance_schema))
        assert len(field_id) == 1
        field_id = int(field_id[0])

        new_datafile.fields = [field_id]
        new_datafile.column_indices = [0]

        return self.fragment_id, new_datafile


FragmentWriter: ray.actor.ActorClass = cast(ray.actor.ActorClass, FragmentWriter)


def run_ray_add_column(
    uri: str,
    columns: list[str],
    transforms: dict[str, UDF],
    checkpoint_store: CheckpointStore,
    /,
    job_id: str | None = None,
    batch_size: int = 8,
    read_version: int | None = None,
    concurrency: int = 8,
    applier_batch_size: int = 32,
    test_run: bool = True,
    **kwargs,
) -> None:
    if read_version is None:
        read_version = lance.dataset(uri).version

    job_id = job_id or uuid.uuid4().hex

    applier = LanceRecordBatchUDFApplier(
        udfs=transforms,
        checkpoint_store=checkpoint_store,
        error_logger=CheckpointStoreErrorLogger(job_id, checkpoint_store),
        batch_size=applier_batch_size,
    )

    pool = ray.util.ActorPool(
        [ApplierActor.remote(applier=applier) for _ in range(concurrency)]
    )

    plan = plan_read(
        uri,
        columns,
        batch_size=batch_size,
        read_version=read_version,
        **kwargs,
    )

    applier_iter = pool.map_unordered(
        lambda actor, value: actor.run.remote(value),
        # the API says list, but iterables are fine
        plan,
    )

    writers = {}
    writer_queues: dict[int, ray.util.queue.Queue] = {}
    writer_futs = {}

    applier_pbar = tqdm(applier_iter, total=len(plan), position=0)
    applier_pbar.set_description("Applying UDFs")

    writer_pbar = tqdm(total=len(writers), position=1)
    writer_pbar.set_description("Writing Fragments")

    def _commit(frags) -> None:
        nonlocal read_version
        _LOG.info("Committing %d fragments", len(ready))
        frags = ray.get(frags)
        operation = lance.LanceOperation.DataReplacement(
            replacements=[
                lance.LanceOperation.DataReplacementGroup(
                    fragment_id=frag_id,
                    new_file=new_file,
                )
                for frag_id, new_file in frags
            ]
        )
        lance.LanceDataset.commit(uri, operation, read_version=read_version)
        read_version += 1
        for frag_id, _ in frags:
            del writers[frag_id]
            del writer_queues[frag_id]
            del writer_futs[frag_id]
            writer_pbar.update(1)

    for item in applier_pbar:
        task: ReadTask = item[0]
        result = item[1]

        frag_id = task.frag_id
        if frag_id not in writers:
            _LOG.info("Creating writer for fragment %d", frag_id)
            queue = ray.util.queue.Queue()
            writer = FragmentWriter.remote(
                uri, list(transforms.keys())[0], checkpoint_store, frag_id, queue
            )
            writer_queues[frag_id] = queue
            writers[frag_id] = writer
            writer_futs[frag_id] = writer.write.remote()
        queue = writer_queues[frag_id]

        queue.put((task.offset, result))

        ready, _ = ray.wait(list(writer_futs.values()), timeout=0)
        if ready:
            _commit(ready)

    # commit any remaining fragments
    _commit(list(writer_futs.values()))
