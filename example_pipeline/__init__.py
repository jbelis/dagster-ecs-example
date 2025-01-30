from dagster import Definitions, AssetSelection, define_asset_job
from example_pipeline.assets import csv_asset, parquet_asset, csv_copy_asset
from example_pipeline.polars_assets import polars_csv_asset, polars_parquet_asset, polars_csv_copy_asset
from example_pipeline.s3_io_manager import S3CSVIOManager, S3ParquetIOManager, S3CSVPolarsIOManager, S3ParquetPolarsIOManager

job = define_asset_job(name="pandas_job", selection=AssetSelection.groups("pandas"))
polars_job = define_asset_job(name="polars_job", selection=AssetSelection.groups("polars"))

defs = Definitions(
    assets=[csv_asset, parquet_asset, csv_copy_asset, polars_csv_asset, polars_parquet_asset, polars_csv_copy_asset],
    resources={
        "parquet_io_manager": S3ParquetIOManager(),
        "csv_io_manager": S3CSVIOManager(),
        "polars_parquet_io_manager": S3ParquetPolarsIOManager(),
        "polars_csv_io_manager": S3CSVPolarsIOManager()
    },
    jobs = [job, polars_job]
)
