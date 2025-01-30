import os
import polars as pl
from dagster import asset, AssetKey, AssetSpec
import example_pipeline.config as config

source_path = os.getenv("SOURCE_FILENAME")
source_name = os.path.splitext(os.path.basename(source_path))[0]
aws_bucket = os.getenv("AWS_BUCKET")


polars_csv_asset = AssetSpec(
    key = AssetKey("polars_csv_asset"),
    group_name="polars",
    metadata = {
        "dagster/io_manager_key": "polars_csv_io_manager", 
        config.S3_URL_METADATA_KEY: f"s3://{aws_bucket}/{source_path}"
    }
)


@asset(group_name="polars", io_manager_key="polars_parquet_io_manager", metadata={
        config.S3_URL_METADATA_KEY: f"s3://{aws_bucket}/out/parquet/{source_name}.parquet"
})
def polars_parquet_asset(polars_csv_asset: pl.DataFrame):
    return polars_csv_asset


@asset(group_name="polars", io_manager_key="polars_csv_io_manager", metadata={
        config.S3_URL_METADATA_KEY: f"s3://{aws_bucket}/out/csv/{source_name}.csv"
})
def polars_csv_copy_asset(polars_parquet_asset: pl.DataFrame):
    return polars_parquet_asset
