import os
import pandas as pd
from dagster import io_manager, OutputContext, InputContext, ConfigurableIOManager
from typing import ClassVar

@io_manager
class RawLocalFileIOManager(ConfigurableIOManager):

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def handle_output(self, context: OutputContext, obj):
        filepath = os.path.join(self.base_dir, *context.asset_key.path)
        context.log.info(f"Writing data to {filepath}")

        # Write the data to a file
        with open(filepath, "w") as f:
            f.write(str(obj))

    def load_input(self, context: InputContext):
        filepath = os.path.join(self.base_dir, *context.asset_key.path)
        context.log.info(f"Reading data from {filepath}")

        # Read the data from the file
        with open(filepath, "r") as f:
            return f.read()
        

@io_manager
class LocalCSVIOManager(ConfigurableIOManager):
    base_dir: ClassVar[str] = os.getenv("DATA_DIR")

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        # Use the asset key to determine the file name
        filepath = f"{os.path.join(self.base_dir, *context.asset_key.path)}.csv"
        context.log.info(f"Saving DataFrame to {filepath}")
        obj.to_csv(filepath, index=False)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        filepath = f"{os.path.join(self.base_dir, *context.asset_key.path)}.csv"
        context.log.info(f"Loading DataFrame from {filepath}")
        return pd.read_csv(filepath)


@io_manager
class LocalParquetIOManager(ConfigurableIOManager):
    base_dir: ClassVar[str] = os.getenv("DATA_DIR")

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        filepath = f"{os.path.join(self.base_dir, *context.asset_key.path)}.parquet"
        context.log.info(f"Saving DataFrame to {filepath}")
        obj.to_parquet(f"{filepath}")

    def load_input(self, context: InputContext) -> pd.DataFrame:
        filepath = f"{os.path.join(self.base_dir, *context.asset_key.path)}.parquet"
        context.log.info(f"Loading DataFrame from {filepath}")
        return pd.read_parquet(f"{filepath}")
    
