from hwp.assets import parquet_asset
import pandas as pd

def test_asset():
    df = pd.DataFrame(
        [
            {"title": "Wow, Dagster is such an awesome and amazing product. I can't wait to use it!"},
            {"title": "Pied Piper launches new product"},
        ]
    )
    results = parquet_asset(df)
    assert results is not None # It returned something

