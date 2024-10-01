from dagster import ExecuteInProcessResult
from hwp import defs
from hwp.assets import parquet_asset
import pandas as pd

def test_job():
    jd = defs.get_job_def(name="example_job")
    result = jd.execute_in_process()

    # return type is ExecuteInProcessResult
    assert isinstance(result, ExecuteInProcessResult)
    assert result.success

    print(result)
    # inspect individual op result
    #assert result.output_for_node("add_one") == 2
    #assert result.output_for_node("add_two") == 3
    #assert result.output_for_node("subtract") == -1

def test_asset():
    df = pd.DataFrame(
        [
            {"title": "Wow, Dagster is such an awesome and amazing product. I can't wait to use it!"},
            {"title": "Pied Piper launches new product"},
        ]
    )
    results = parquet_asset(df)
    assert results is not None # It returned something

