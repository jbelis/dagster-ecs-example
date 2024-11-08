import os
import pandas as pd
from dagster import asset, AssetKey, AssetSpec

source_path = os.getenv("SOURCE_FILENAME")
print (source_path)
source_filename = os.path.splitext(os.path.basename(source_path))[0]
aws_bucket = os.getenv("AWS_BUCKET")


csv_asset = AssetSpec(
    key = AssetKey("csv_asset"),
    metadata = {
        "dagster/io_manager_key": "csv_io_manager", 
        "dagster/uri": f"s3://{aws_bucket}/{source_path}"
    }
)

@asset(io_manager_key="parquet_io_manager", key=AssetKey(["out", "parquet", source_filename]))
def parquet_asset(csv_asset: pd.DataFrame):
    return csv_asset
