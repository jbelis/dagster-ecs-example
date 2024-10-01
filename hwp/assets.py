import pandas as pd
from dagster import asset, AssetKey, AssetSpec

csv_asset = AssetSpec(
    key = AssetKey(["in", "dropout"]),
    metadata = {"dagster/io_manager_key": "csv_io_manager"},
)

@asset(io_manager_key="parquet_io_manager", key_prefix=["out"])
def parquet_asset(dropout: pd.DataFrame):
    return dropout
