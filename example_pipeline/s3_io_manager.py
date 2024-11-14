import os
from dagster import io_manager, InputContext, OutputContext, ConfigurableIOManager
import pandas as pd
from typing import ClassVar
import example_pipeline.config as config


class _S3IOManager(ConfigurableIOManager):
    bucket: ClassVar[str] = os.getenv("AWS_BUCKET")

    def _s3_input_url(self, context: InputContext) -> str:
        url = None
        # if a input filename is provided, use it
        if context.upstream_output is not None:
            url = context.upstream_output.metadata.get(config.S3_URL_METADATA_KEY)

        # Otherwise construct a url from context path
        if url is None:
            filepath = os.path.join(*context.asset_key.path)
            url = f"s3://{self.bucket}/{filepath}"

        return url

    def _s3_output_url(self, context: OutputContext) -> str:
        if context.metadata is not None:
            url = context.metadata.get(config.S3_URL_METADATA_KEY)

        # Otherwise construct a url from context path
        if url is None:
            filepath = os.path.join(*context.asset_key.path)
            url = f"s3://{self.bucket}/{filepath}"

        return url
    

@io_manager
class S3CSVIOManager(_S3IOManager):

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        url = self._s3_output_url(context)
        context.log.info(f"Writing object to {url}")
        obj.to_csv(url)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        url = self._s3_input_url(context)
        context.log.info(f"Reading csv data from {url}")
        return pd.read_csv(url)


@io_manager
class S3ParquetIOManager(_S3IOManager):

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        url = self._s3_output_url(context)
        context.log.info(f"Writing object to {url}")
        obj.to_parquet(url)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        url = self._s3_input_url(context)
        context.log.info(f"Reading parquet data from {url}")
        return pd.read_parquet(url)

