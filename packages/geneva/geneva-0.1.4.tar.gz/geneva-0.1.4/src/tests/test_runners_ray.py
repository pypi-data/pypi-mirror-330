# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from pathlib import Path

import lance
import pyarrow as pa

from geneva import LanceCheckpointStore, udf
from geneva.runners.ray.pipeline import run_ray_add_column


def test_run_ray_add_column(tmp_path: Path) -> None:
    @udf(data_type=pa.int32(), batch_size=8)
    def add_one(a) -> int:
        return a + 1

    data = {"a": pa.array(range(100))}
    tbl = pa.Table.from_pydict(data)
    ckp_store = LanceCheckpointStore(str(tmp_path / "ckp"))

    tbl_path = tmp_path / "foo.lance"
    ds = lance.write_dataset(tbl, tbl_path)

    def return_none(batch: pa.RecordBatch) -> pa.RecordBatch:
        return pa.RecordBatch.from_pydict(
            {"b": pa.array([None] * batch.num_rows, pa.int32())}
        )

    new_fragment, new_schema = ds.get_fragment(0).merge_columns(
        return_none, columns=["a"]
    )

    merge = lance.LanceOperation.Merge([new_fragment], new_schema)
    lance.LanceDataset.commit(tbl_path, merge, read_version=ds.version)

    run_ray_add_column(str(tbl_path), ["a"], {"b": add_one}, ckp_store)

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == {
        "a": list(range(100)),
        "b": [x + 1 for x in range(100)],
    }
