# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import hashlib
import logging
import random
from collections.abc import Iterator
from typing import TypeVar

import attrs
import lance
import pyarrow as pa

from geneva.checkpoint import (
    CheckpointStore,
)
from geneva.debug.logger import ErrorLogger, NoOpErrorLogger
from geneva.query import Scan
from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)


@attrs.define
class ReadTask:
    uri: str
    columns: list[str]
    frag_id: int
    offset: int
    limit: int

    filter: str | None = None

    batch_size: int = 1024

    def to_batches(self) -> Iterator[pa.RecordBatch]:
        uri_parts = self.uri.split("/")
        name = ".".join(uri_parts[-1].split(".")[:-1])
        db = "/".join(uri_parts[:-1])
        scan = (
            Scan.from_uri(db, name)
            .with_columns(self.columns)
            .with_fragments([self.frag_id])
            .with_filter(self.filter)
            .with_offset(self.offset)
            .with_limit(self.limit)
        )
        yield from scan.to_batches(self.batch_size)

    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"{self.uri}:{self.frag_id}:{self.offset}:{self.limit}:{self.filter}".encode(),
        )
        return hasher.hexdigest()


@attrs.define
class LanceRecordBatchUDFApplier:
    udfs: dict[str, UDF] = attrs.field()
    checkpoint_store: CheckpointStore = attrs.field()
    error_logger: ErrorLogger = attrs.field(default=NoOpErrorLogger())

    @property
    def output_schema(self) -> pa.Schema:
        return pa.schema(
            [pa.field(name, fn.data_type) for name, fn in self.udfs.items()],
        )

    def _run(self, task: ReadTask) -> dict[str, str]:
        data_key = task.checkpoint_key()
        _LOG.debug("Running task %s", task)
        # track the batch sequence number so we can checkpoint any errors
        # when reproducing locally we can seek to the erroring batch quickly

        # prepare the schema
        fields = []
        for name, fn in self.udfs.items():
            fields.append(pa.field(name, fn.data_type, metadata=fn.field_metadata))

        res = {}
        batch = None
        for name, fn in self.udfs.items():
            checkpoint_key = f"{data_key}:{fn.checkpoint_key}"
            if checkpoint_key in self.checkpoint_store:
                _LOG.info("Using cached result for %s", checkpoint_key)
                res[name] = checkpoint_key
                continue
            arrs = []
            # PERF203 -- don't try-except inside the loop
            # so I had to move the loop inside the try-except
            # and need some loop state tracking for error logggin
            seq = 0
            # TODO: add caching for the input data
            try:
                for _seq, batch in enumerate(task.to_batches()):
                    seq = _seq
                    arrs.append(fn(batch))
            except Exception as e:
                self.error_logger.log_error(e, task, fn, seq)
                raise e

            arr = pa.concat_arrays(arrs)
            self.checkpoint_store[checkpoint_key] = pa.RecordBatch.from_pydict(
                {"data": arr},
                schema=pa.schema([pa.field("data", fn.data_type)]),
            )
            res[name] = checkpoint_key

        return res

    def run(self, task: ReadTask) -> dict[str, str]:
        try:
            return self._run(task)
        except Exception as e:
            logging.exception("Error running task %s: %s", task, e)
            raise RuntimeError(f"Error running task {task}") from e

    def status(self, task: ReadTask) -> dict[str, str]:
        data_key = task.checkpoint_key()
        return {
            name: f"{data_key}:{fn.checkpoint_key}" in self.checkpoint_store
            for name, fn in self.udfs.items()
        }  # type: ignore


def _plan_read(
    uri: str,
    columns: list[str] | None = None,
    *,
    read_version: int | None = None,
    batch_size: int = 512,
    filter: str | None = None,  # noqa: A002
) -> Iterator[ReadTask]:
    """Make Plan for Reading Data from a Dataset"""
    if columns is None:
        columns = []
    dataset = lance.dataset(uri)
    if read_version is not None:
        dataset = dataset.checkout_version(read_version)

    for frag in dataset.get_fragments():
        frag_rows = frag.count_rows(filter=filter)
        for offset in range(0, frag_rows, batch_size):
            limit = min(batch_size, frag_rows - offset)
            yield ReadTask(
                uri=uri,
                columns=columns,
                frag_id=frag.fragment_id,
                batch_size=batch_size,
                offset=offset,
                limit=limit,
                filter=filter,
            )


@attrs.define
class _LanceReadPlanIterator(Iterator[ReadTask]):
    it: Iterator[ReadTask]
    total: int

    def __iter__(self) -> Iterator[ReadTask]:
        return self

    def __next__(self) -> ReadTask:
        return next(self.it)

    def __len__(self) -> int:
        return self.total


def _num_tasks(
    *,
    uri: str,
    read_version: int | None = None,
    batch_size: int = 512,
) -> int:
    return sum(
        -(-frag.count_rows() // batch_size)
        for frag in (lance.dataset(uri, version=read_version)).get_fragments()
    )


T = TypeVar("T")


def _buffered_shuffle(it: Iterator[T], buffer_size: int) -> Iterator[T]:
    """Shuffle an iterator using a buffer of size buffer_size
    not perfectly random, but good enough for spreading out IO
    """
    # Initialize the buffer with the first buffer_size items from the iterator
    buffer = []
    # Fill the buffer with up to buffer_size items initially
    try:
        for _ in range(buffer_size):
            item = next(it)
            buffer.append(item)
    except StopIteration:
        pass

    while True:
        # Select a random item from the buffer
        index = random.randint(0, len(buffer) - 1)
        item = buffer[index]

        # Try to replace the selected item with a new one from the iterator
        try:
            next_item = next(it)
            buffer[index] = next_item
            # Yield the item AFTER replacing it in the buffer
            # this way the buffer is always contiguous so we can
            # simply yield the buffer at the end
            yield item
        except StopIteration:
            yield from buffer
            break


def plan_read(
    uri: str,
    columns: list[str] | None = None,
    *,
    read_version: int | None = None,
    batch_size: int = 512,
    filter: str | None = None,  # noqa: A002
    shuffle_buffer_size: int = 0,
) -> Iterator[ReadTask]:
    """Make Plan for Reading Data from a Dataset"""
    it = _plan_read(
        uri,
        columns=columns,
        read_version=read_version,
        batch_size=batch_size,
        filter=filter,
    )
    # same as no shuffle
    if shuffle_buffer_size > 1:
        it = _buffered_shuffle(it, buffer_size=shuffle_buffer_size)

    return _LanceReadPlanIterator(
        it, _num_tasks(uri=uri, read_version=read_version, batch_size=batch_size)
    )
