from dagster import execute_job, DagsterInstance, reconstructable, ExecuteInProcessResult
from example_pipeline import defs

def return_job_def():
    return defs.get_job_def(name="example_job")

def run() -> ExecuteInProcessResult:
    #execute_job(reconstructable(return_job_def), instance=DagsterInstance.get())
    return return_job_def().execute_in_process()