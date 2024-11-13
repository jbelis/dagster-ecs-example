import os
from dotenv import load_dotenv
from dagster import Definitions, AssetSelection, define_asset_job
from example_pipeline.assets import csv_asset, parquet_asset
from example_pipeline.s3_io_manager import S3CSVIOManager, S3ParquetIOManager

job = define_asset_job(name="example_job", selection=AssetSelection.all())

defs = Definitions(
    assets=[csv_asset, parquet_asset],
    resources={
        "parquet_io_manager": S3ParquetIOManager(),
        "csv_io_manager": S3CSVIOManager()
    },
    jobs = [job]
)
