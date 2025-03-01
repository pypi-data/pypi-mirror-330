# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# Test data lake works with PyTorch

from pathlib import Path

import lance
import lance.torch.data
import pyarrow as pa
import torch

from geneva import connect


def test_torch_dataset(tmp_path: Path) -> None:
    db = connect(tmp_path)
    data = pa.Table.from_pydict({"a": [1, 2, 3], "b": [4, 5, 6]})

    tbl = db.create_table("test", data)

    ds = lance.torch.data.LanceDataset(tbl, batch_size=2)

    tensor = next(iter(ds))
    assert torch.equal(tensor["a"], torch.tensor([1, 2]))
    assert torch.equal(tensor["b"], torch.tensor([4, 5]))
