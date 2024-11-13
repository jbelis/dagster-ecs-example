from dagster import ExecuteInProcessResult
from example_pipeline import defs
import logging

"""in-process job executor
"""

logger = logging.getLogger(__name__)

#def return_job_def():
#    return defs.get_job_def(name="example_job")

def run() -> ExecuteInProcessResult:
    jd = defs.get_job_def(name="example_job")
    logger.info(f"Executing {jd.name}")
    #execute_job(reconstructable(return_job_def), instance=DagsterInstance.get())
    return jd.execute_in_process()