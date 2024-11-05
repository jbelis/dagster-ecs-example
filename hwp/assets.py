import os
import pandas as pd
from dagster import asset, AssetKey, AssetSpec

source_filename = os.getenv("SOURCE_FILENAME")
aws_bucket = os.getenv("AWS_BUCKET")

csv_asset = AssetSpec(
    key = AssetKey("csv_asset"),
    metadata = {
        "dagster/io_manager_key": "csv_io_manager", 
        "dagster/uri": f"s3://{aws_bucket}/{source_filename}"
    }
)

@asset(io_manager_key="parquet_io_manager", key_prefix=["out"])
def parquet_asset(csv_asset: pd.DataFrame):
    return csv_asset
