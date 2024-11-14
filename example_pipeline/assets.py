import os
import pandas as pd
from dagster import asset, AssetKey, AssetSpec
import example_pipeline.config as config

source_path = os.getenv("SOURCE_FILENAME")
source_name = os.path.splitext(os.path.basename(source_path))[0]
aws_bucket = os.getenv("AWS_BUCKET")


csv_asset = AssetSpec(
    key = AssetKey("csv_asset"),
    metadata = {
        "dagster/io_manager_key": "csv_io_manager", 
        config.S3_URL_METADATA_KEY: f"s3://{aws_bucket}/{source_path}"
    }
)


@asset(io_manager_key="parquet_io_manager", metadata={
        config.S3_URL_METADATA_KEY: f"s3://{aws_bucket}/out/parquet/{source_name}.parquet"
})
def parquet_asset(csv_asset: pd.DataFrame):
    return csv_asset


@asset(io_manager_key="csv_io_manager", metadata={
        config.S3_URL_METADATA_KEY: f"s3://{aws_bucket}/out/csv/{source_name}.csv"
})
def csv_copy_asset(parquet_asset: pd.DataFrame):
    return parquet_asset
