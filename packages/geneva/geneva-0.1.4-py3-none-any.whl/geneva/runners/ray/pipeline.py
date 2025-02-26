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


def _write_fragment(
    uri: str,
    column_name: str,
    store: CheckpointStore,
    checkpoint_keys: Iterator[dict[str, str]],
) -> lance.fragment.DataFile:
    dataset = lance.dataset(uri)
    import more_itertools

    def _iter() -> Iterator[pa.RecordBatch]:
        for batch in checkpoint_keys:
            res = {
                key: _combine_chunks(store[value]["data"])
                for key, value in batch.items()
            }
            yield pa.RecordBatch.from_pydict(res)

    it = more_itertools.peekable(_iter())
    rbr = pa.RecordBatchReader.from_batches(it.peek().schema, it)

    # TODO: this doesn't support struct or complex schema yet
    new_data = lance.fragment.write_fragments(
        rbr,
        uri,
        max_rows_per_file=1 << 31,
        max_bytes_per_file=1 << 40,
    )

    assert len(new_data) == 1
    new_data = new_data[0]
    assert len(new_data.files) == 1
    new_datafile = new_data.files[0]

    # MASSIVE HACK: open up an API to get the field id from the column name
    field_id = re.compile(rf'name: "{column_name}", id: (?P<field_id>[\d]*),').findall(
        str(dataset.lance_schema)
    )
    assert len(field_id) == 1
    field_id = int(field_id[0])

    new_datafile.fields = [field_id]
    new_datafile.column_indices = [0]

    return new_datafile


@ray.remote
@attrs.define
class ApplierActor:
    applier: LanceRecordBatchUDFApplier

    def run(self, task) -> tuple[ReadTask, dict[str, str]]:
        return task, self.applier.run(task)


ApplierActor: ray.actor.ActorClass = cast(ray.actor.ActorClass, ApplierActor)


@ray.remote
@attrs.define
class FragementWriter:
    uri: str
    column_name: str
    store: CheckpointStore

    frags: list = attrs.field(factory=list)

    written: bool = attrs.field(init=False, default=False)

    def write(self) -> lance.fragment.DataFile:
        if self.written:
            raise RuntimeError("Already written")

        def _key_iter() -> Iterator[dict[str, str]]:
            while self.frags:
                _, item = heapq.heappop(self.frags)
                yield item

        file = _write_fragment(self.uri, self.column_name, self.store, _key_iter())
        self.written = True
        return file

    def add_task_result(self, task: ReadTask, result) -> None:
        if self.written:
            raise RuntimeError("Already written")

        heapq.heappush(self.frags, (task.offset, result))


FragementWriter: ray.actor.ActorClass = cast(ray.actor.ActorClass, FragementWriter)


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
    plan_shuffle_buffer_size: int = 1024,
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
    )

    pool = ray.util.ActorPool(
        [ApplierActor.remote(applier=applier) for _ in range(concurrency)]
    )

    plan = plan_read(
        uri,
        columns,
        batch_size=batch_size,
        read_version=read_version,
        shuffle_buffer_size=plan_shuffle_buffer_size,
    )

    applier_iter = pool.map_unordered(
        lambda actor, value: actor.run.remote(value),
        # the API says list, but iterables are fine
        plan,
    )

    ds = lance.dataset(uri, version=read_version)
    writers = {
        frag.fragment_id: FragementWriter.remote(
            uri, list(transforms.keys())[0], checkpoint_store
        )
        for frag in ds.get_fragments()
    }

    applier_pbar = tqdm(applier_iter, total=len(plan))
    applier_pbar.set_description("Applying UDFs")

    futs = []
    for item in applier_pbar:
        task: ReadTask = item[0]
        result = item[1]

        frag_id = task.frag_id
        writer = writers[frag_id]
        futs.append(writer.add_task_result.remote(task, result))
    ray.wait(futs)

    writers = {frag_id: writer.write.remote() for frag_id, writer in writers.items()}

    _LOG.info("Committing %d fragments", len(writers))

    writer_pbar = tqdm(writers.items(), total=len(writers))
    writer_pbar.set_description("Writing Fragments")

    operation = lance.LanceOperation.DataReplacement(
        replacements=[
            lance.LanceOperation.DataReplacementGroup(
                fragment_id=frag_id,
                new_file=ray.get(writer),
            )
            for frag_id, writer in writer_pbar
        ]
    )

    lance.LanceDataset.commit(uri, operation, read_version=read_version)
