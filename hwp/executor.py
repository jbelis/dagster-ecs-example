from dagster import execute_job, DagsterInstance, reconstructable
from hwp import defs

def return_job_def():
    return defs.get_job_def(name="example_job")

def run():
    execute_job(reconstructable(return_job_def), instance=DagsterInstance.get())
