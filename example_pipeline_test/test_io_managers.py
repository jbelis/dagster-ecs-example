from dagster import AssetKey, OutputContext, InputContext
from example_pipeline import S3CSVIOManager, config, S3ParquetIOManager
import os
import pytest


bucket = os.getenv("AWS_BUCKET")

@pytest.mark.parametrize(
    "iomanager, filename",
    [
        (S3CSVIOManager(), "file.csv"),
        (S3ParquetIOManager(), "file.parquet")
    ]
)
def test_s3_output_url_without_metadata(iomanager, filename):
    context = OutputContext(
        asset_key=AssetKey(["prefix", filename]),
        metadata={}
    )
    assert iomanager._s3_output_url(context) == f"s3://{bucket}/prefix/{filename}"


def test_s3_output_url_with_metadata():
    context = OutputContext(
        asset_key=AssetKey("asset"),
        metadata={config.S3_URL_METADATA_KEY: f"s3://{bucket}/prefix/path.csv"}
    )
    iomanager = S3CSVIOManager()
    assert iomanager._s3_output_url(context) == f"s3://{bucket}/prefix/path.csv"


def test_s3_input_url_without_metadata():
    context = InputContext(
        asset_key=AssetKey(["prefix", "path.csv"]),
        metadata={}
    )
    iomanager = S3CSVIOManager()
    assert iomanager._s3_input_url(context) == f"s3://{bucket}/prefix/path.csv"

def test_s3_input_url_with_metadata():
    context = InputContext(
        asset_key=AssetKey("asset"),
        upstream_output = OutputContext(
            metadata={config.S3_URL_METADATA_KEY: f"s3://{bucket}/prefix/path.csv"}
        )
    )
    iomanager = S3CSVIOManager()
    assert iomanager._s3_input_url(context) == f"s3://{bucket}/prefix/path.csv"