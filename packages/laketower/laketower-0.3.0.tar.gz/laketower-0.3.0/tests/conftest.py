from pathlib import Path
from typing import Any

import deltalake
import numpy as np
import pandas as pd
import pytest
import yaml


@pytest.fixture()
def delta_table_data() -> pd.DataFrame:
    periods = 24
    daterange = pd.date_range(
        start="2025-01-01T00:00:00+00:00", periods=periods, freq="1h"
    )
    temperature = np.round(np.linspace(-5, -5 + periods, num=periods))
    return pd.DataFrame(
        {"time": daterange, "city": "Grenoble", "temperature": temperature}
    )


@pytest.fixture()
def delta_table(tmp_path: Path, delta_table_data: pd.DataFrame) -> deltalake.DeltaTable:
    table_path = tmp_path / "delta_table"
    schema = deltalake.Schema(
        [
            deltalake.Field("time", "timestamp_ntz", nullable=False),  # type: ignore[arg-type]
            deltalake.Field("city", "string", nullable=False),  # type: ignore[arg-type]
            deltalake.Field("temperature", "float", nullable=False),  # type: ignore[arg-type]
        ]
    )
    dt = deltalake.DeltaTable.create(
        table_path, schema, name="delta_table", description="Sample Delta Table"
    )
    deltalake.write_deltalake(dt, delta_table_data, mode="append")
    return dt


@pytest.fixture()
def sample_config(delta_table: deltalake.DeltaTable) -> dict[str, Any]:
    return {
        "tables": [
            {"name": "delta_table", "uri": delta_table.table_uri, "format": "delta"}
        ]
    }


@pytest.fixture()
def sample_config_path(tmp_path: Path, sample_config: dict[str, Any]) -> Path:
    config_path = tmp_path / "laketower.yml"
    config_path.write_text(yaml.dump(sample_config))
    return config_path
