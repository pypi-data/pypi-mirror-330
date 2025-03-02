import logging
import json
import subprocess
import functools
from pathlib import Path
from typing import Union, List

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

# TODO understand more about threading.Thread vs multiprocessing.Process:
# https://discuss.dizzycoding.com/python-subprocess-callback-when-cmd-exits/

from concurrent.futures import ThreadPoolExecutor as Pool


"""
def callback(
    cmds_to_run_next: List[List[str]],
    log_dir: Union[Path, str],
    log_prefix: str,
    future,
):
    if future.exception() is not None:
        logger.info(f"previous process exception: {future.exception()}")
    else:
        logger.info(f"previous process returned {future.result()}")
        start_chain_subprocesses(cmds_to_run_next, log_dir, log_prefix)
"""


# def start_chain_subprocesses(
#     cmds_to_run: List[List[str]], log_dir: Union[Path, str], log_prefix=""
# ):
#     # wait for the process completion asynchronously
#     logger.info("begin waiting")
#     logger.info("Starting chain subprocess ...")
#     logger.info(f"Got cmds_to_run: {printify(cmds_to_run)}")
#     logger.info(f"Log dir: {log_dir}")

#     # pool = Pool(
#     #     max_workers=1
#     # )  # Works when this is global, but cannot continue submitting after 'shutdown'
#     pool = app_pool.get_pool()
#     # first_process = start_subprocess(cmds_to_run[0], log_dir, log_prefix)
#     submitted_pool_tasks = []
#     for cmd_to_run in cmds_to_run:
#         res = pool.apply_async(start_subprocess, [cmds_to_run, log_dir, log_prefix])
#         submitted_pool_tasks.append(res)
#     logger.info("Submitted render tasks to pool")
#     return submitted_pool_tasks


# TODO maybe make this recursive with a wait=False arg that can be set to True when
# self-calling.
# This would allow the first process to be passed to the but the said process (which is
# associated with a particular task) will wait for all tasks, as a single item in the pool)?
# If this works, it would be a nice way to control "one job submission at a time".
# def start_chain_subprocesses(
#     cmds_to_run: List[List[str]], log_dir: Union[Path, str], log_prefix=""
# ):
#     # wait for the process completion asynchronously
#     logger.info("begin waiting")
#     logger.info("Starting chain subprocess ...")
#     logger.info(f"Got cmds_to_run: {printify(cmds_to_run)}")
#     logger.info(f"Log dir: {log_dir}")

#     pool = Pool(
#         max_workers=1
#     )  # Works when this is global, but cannot continue submitting after 'shutdown'
#     first_process = start_subprocess(cmds_to_run[0], log_dir, log_prefix)
#     pool.submit(wait_for_process, first_process)
#     if len(cmds_to_run) <= 1:
#         pool.shutdown(wait=False)  # no .submit() calls after that point
#         return first_process
#     for task_arglist in cmds_to_run[1:]:
#         # current_subprocess = start_subprocess(cmds_to_run[0], log_dir, log_prefix)
#         # f = pool.submit(wait_for_process, current_subprocess)
#         pool.submit(start_subprocess, task_arglist, log_dir, log_prefix, wait=False)
#     pool.shutdown(wait=False)  # no .submit() calls after that point
#     logger.info("Submitted render tasks to pool")
#     return first_process


def wait_for_process(process):
    process.communicate()
    # logger.info(f"process.poll(): {process.poll()}")
    return  # process.poll()


def start_subprocess(
    cmd_to_run: List[str], log_dir: Union[Path, str], log_prefix="", wait=True
) -> subprocess.Popen:
    logger.info("Starting subprocess ...")

    # Prepare logging
    logger.info(f"Log dir: {log_dir}")
    if not log_prefix:
        log_prefix = cmd_to_run[0] + "_"
    if not Path(log_dir).exists():
        logger.info(f"Creating dir: {log_dir}")
        Path(log_dir).mkdir(parents=True)
    log_stdout = f"{log_dir}/{log_prefix}stdout.log"
    log_stderr = f"{log_dir}/{log_prefix}stderr.log"

    # Remove any empty items from cmd_to_run
    cmd_to_run = [item for item in cmd_to_run if item != ""]
    logger.info(f"running cmd:\n{json.dumps(cmd_to_run, indent=2)}")

    # Execute
    try:
        with open(log_stdout, "wb") as out, open(log_stderr, "wb") as err:
            process = subprocess.Popen(cmd_to_run, stdout=out, stderr=err)
    except Exception as e:
        logger.exception(f"Caught an error: {e}")
        raise e
    logger.info(f"Started new process: {process}")
    if wait:
        logger.info(f"Waiting for process: {process} ...")
        process.communicate()
    return process
