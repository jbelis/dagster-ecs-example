import os
from dagster import io_manager, InputContext, OutputContext, ConfigurableIOManager
import pandas as pd
from typing import ClassVar

class _S3IOManager(ConfigurableIOManager):
    bucket: ClassVar[str] = os.getenv("AWS_BUCKET")
    credentials: ClassVar[dict] = {
        "key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "token": os.getenv("AWS_SESSION_TOKEN")
    }

    def _s3_url(self, context, suffix = "") -> str:
        filepath = os.path.join(*context.asset_key.path)
        context.log.info(f"Writing object to s3://{self.bucket}/{filepath}{suffix}")
        return f"s3://{self.bucket}/{filepath}{suffix}"


@io_manager
class S3CSVIOManager(_S3IOManager):

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        url = self._s3_url(context, ".csv")
        obj.to_csv(url, storage_options=self.credentials)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        url = self._s3_url(context, ".csv")        
        return pd.read_csv(url, storage_options=self.credentials)


@io_manager
class S3ParquetIOManager(_S3IOManager):

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        url = self._s3_url(context, ".parquet")
        obj.to_parquet(url, storage_options=self.credentials)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        url = self._s3_url(context, ".parquet")
        return pd.read_parquet(url, storage_options=self.credentials)

