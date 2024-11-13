from dagster import ExecuteInProcessResult, reconstructable, DagsterInstance, execute_job
from example_pipeline import defs
import logging

"""out-of-process executor
"""

logger = logging.getLogger(__name__)

def return_job_def():
    return defs.get_job_def(name="example_job")

def run() -> ExecuteInProcessResult:
    return execute_job(reconstructable(return_job_def), instance=DagsterInstance.get())
