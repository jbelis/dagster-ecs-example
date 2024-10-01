from dotenv import load_dotenv
from dagster import Definitions, AssetSelection, define_asset_job
from hwp.assets import csv_asset, parquet_asset
from hwp.s3_io_manager import S3CSVIOManager, S3ParquetIOManager

print("__INIT__ EXECUTING")
load_dotenv()  # take environment variables from .env

job = define_asset_job(name="example_job", selection=AssetSelection.all())

defs = Definitions(
    assets=[csv_asset, parquet_asset],
    resources={
        "parquet_io_manager": S3ParquetIOManager(),
        "csv_io_manager": S3CSVIOManager()
    },
    jobs = [job]
)
