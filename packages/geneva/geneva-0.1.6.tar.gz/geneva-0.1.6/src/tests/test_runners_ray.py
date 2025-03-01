# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import itertools
from pathlib import Path

import lance
import pyarrow as pa
import pytest

from geneva import LanceCheckpointStore, udf
from geneva.runners.ray.pipeline import run_ray_add_column


@pytest.mark.parametrize(
    "shuffle_config",
    [
        {
            "applier_batch_size": applier_batch_size,
            "batch_size": batch_size,
            "shuffle_buffer_size": shuffle_buffer_size,
            "task_shuffle_diversity": task_shuffle_diversity,
        }
        for (
            applier_batch_size,
            batch_size,
            shuffle_buffer_size,
            task_shuffle_diversity,
        ) in itertools.product(
            [1, 2, 3],
            range(1, 5),
            [0, 1, 3, 16],
            [None, 1, 3, 16],
        )
    ],
)
def test_run_ray_add_column(tmp_path: Path, shuffle_config) -> None:
    @udf(data_type=pa.int32(), batch_size=8)
    def add_one(a) -> int:
        return a + 1

    data = {"a": pa.array(range(256))}
    tbl = pa.Table.from_pydict(data)
    ckp_store = LanceCheckpointStore(str(tmp_path / "ckp"))

    tbl_path = tmp_path / "foo.lance"
    ds = lance.write_dataset(tbl, tbl_path, max_rows_per_file=16)

    def return_none(batch: pa.RecordBatch) -> pa.RecordBatch:
        return pa.RecordBatch.from_pydict(
            {"b": pa.array([None] * batch.num_rows, pa.int32())}
        )

    new_frags = []
    new_schema = None
    for frag in ds.get_fragments():
        new_fragment, new_schema = frag.merge_columns(return_none, columns=["a"])
        new_frags.append(new_fragment)

    assert new_schema is not None
    merge = lance.LanceOperation.Merge(new_frags, new_schema)
    lance.LanceDataset.commit(tbl_path, merge, read_version=ds.version)

    run_ray_add_column(
        str(tbl_path), ["a"], {"b": add_one}, ckp_store, **shuffle_config
    )

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == {
        "a": list(range(256)),
        "b": [x + 1 for x in range(256)],
    }
