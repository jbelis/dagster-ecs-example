import os
from dagster import io_manager, InputContext, OutputContext, ConfigurableIOManager
import pandas as pd
from typing import ClassVar
import json

class _S3IOManager(ConfigurableIOManager):
    bucket: ClassVar[str] = os.getenv("AWS_BUCKET")
    credentials: ClassVar[dict] = {
        "key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "token": os.getenv("AWS_SESSION_TOKEN")
    }

    def _s3_input_url(self, context: InputContext, suffix = "") -> str:
        url = None
        # if a input filename is provided, use it
        if context.upstream_output != None:
            uri = context.upstream_output.metadata.get("dagster/uri")
            if uri != None:
                url = f"{uri}{suffix}"

        # Otherwise construct a url from context path
        if url == None:
            filepath = os.path.join(*context.asset_key.path)
            url = f"s3://{self.bucket}/{filepath}{suffix}"

        return url

    def _s3_url(self, context: OutputContext, suffix = "") -> str:
        filepath = os.path.join(*context.asset_key.path)
        return f"s3://{self.bucket}/{filepath}{suffix}"


@io_manager
class S3CSVIOManager(_S3IOManager):

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        url = self._s3_url(context, ".csv")
        context.log.info(f"Writing object to {url}")
        obj.to_csv(url, storage_options=self.credentials)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        url = self._s3_input_url(context, ".csv")
        context.log.info(f"Reading data from {url}")
        return pd.read_csv(url, storage_options=self.credentials)


@io_manager
class S3ParquetIOManager(_S3IOManager):

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        url = self._s3_url(context, ".parquet")
        context.log.info(f"Writing object to {url}")
        obj.to_parquet(url, storage_options=self.credentials)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        url = self._s3_input_url(context, ".parquet")
        context.log.info(f"Reading data from {url}")
        return pd.read_parquet(url, storage_options=self.credentials)

