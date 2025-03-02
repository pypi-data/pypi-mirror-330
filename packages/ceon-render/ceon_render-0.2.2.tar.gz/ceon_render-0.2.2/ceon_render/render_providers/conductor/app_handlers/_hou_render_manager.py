# TODO this is legacy code. Refactor for local rendering workflow
import os
import logging
import subprocess
from pathlib import Path

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

CSTOCK_STORAGE_DIR = os.getenv("CSTOCK_STORAGE_DIR")
CSTOCK_APP_DIR = os.getenv("CSTOCK_APP_DIR")
RENDER_MODE = os.getenv("RENDER_MODE")

jobs_path = f"{CSTOCK_STORAGE_DIR}/jobs"
script_run_render = f"{CSTOCK_APP_DIR}/utility/render/run_render_hython.py"

job_processes = {}

# TODO improve logfile parsing
def parse_log_file(log_file):
    result = subprocess.run(["tail", str(log_file)], stdout=subprocess.PIPE)
    result_lines = result.stdout.decode("utf-8").splitlines()
    if len(result_lines) > 1:
        if result_lines[-1] == "Render Complete":
            return "Complete"
        elif "ALF_PROGRESS" in result_lines[-1]:
            return result_lines[-1].split()[-1]
        else:
            return "OTHER: " + result_lines[-1]
    else:
        return "Empty log file found"


def file_has_content(file_path):
    return os.path.exists(file_path) and not os.stat(file_path).st_size == 0


def check_render_progress(job_id):
    # TODO poll the running process to see if process is 'complete' in the case that there was an error
    # TODO refactor to use job_object

    process = job_processes[job_id]
    # subprocess.poll() returns None if process has not terminated
    process_poll = process.poll()
    in_progress = process_poll == None

    log_file = Path(f"{jobs_path}/{job_id}/logs/{job_id}_render_stdout.txt").resolve()
    log_file_errors = Path(
        f"{jobs_path}/{job_id}/logs/{job_id}_render_stderr.txt"
    ).resolve()

    code = 0
    message = "Checking for log file"

    if log_file.is_file():
        if in_progress:
            message = parse_log_file(log_file)
        else:
            if process_poll != 0:
                code = -1
                message = "Failed"
            else:
                if file_has_content(log_file_errors):
                    code = 2
                    message = "Complete, with errors"
                else:
                    code = 1
                    message = "Complete"
    else:
        message = "Log file not found: " + str(log_file)
    # -1: Failed, 0-running, 1-complete, 2-complete with errors
    return [code, message]


def run_local_render(job_object):
    job_id = job_object.job_id
    proj_id = job_object.proj_id

    job_path = job_object.dirs["root"]

    if not os.path.exists(job_path):
        os.makedirs(job_path)

    log_stdout = f"{job_path}/logs/{job_id}_render_stdout.txt"
    log_stderr = f"{job_path}/logs/{job_id}_render_stderr.txt"

    vars_to_set = [
        f"CSTOCK_INPUTS_FOLDER={job_path}/inputs",
        f"CSTOCK={job_path}/inputs",
    ]

    try:
        cmd_to_run = ["hython", script_run_render, str(job_id), str(proj_id)] + list(
            vars_to_set
        )
        with open(log_stdout, "wb") as out, open(log_stderr, "wb") as err:
            process = subprocess.Popen(cmd_to_run, stdout=out, stderr=err)
        # subprocess.Popen(["hython", script_run_render]);
        new_job = {job_id: process}
        job_processes.update(new_job)
        print("Started new process. All processes: ", job_processes)
        return 1
    except Exception as e:
        logging.exception("Caught an error")
        return "Failed to submit local render: ".format(str(e))


def begin_local_render(job_object, saved_user_args):
    print("Submitting render...")
    job_id = job_object.job_id
    # proj_id = job_object.proj_id

    job_path = f"{jobs_path}/{job_id}/"
    if not os.path.exists(job_path):
        os.makedirs(job_path)

    print(f"Submitting to local render (job_id: {job_id})...")
    return run_local_render(job_object)
