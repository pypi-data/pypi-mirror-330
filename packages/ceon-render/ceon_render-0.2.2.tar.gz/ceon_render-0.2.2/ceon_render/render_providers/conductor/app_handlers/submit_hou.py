import logging
from pathlib import Path

from .render_args import RenderArgsHou

from app.execute import start_subprocess
from app.job_queue import q

from .render import create_cmdline_args

logger = logging.getLogger(__name__)

def submit(render_args_hou: RenderArgsHou):
    # app_render_args = render.ffmpeg.create_render_args(payload)
    # cmdline_args = render.ffmpeg.create_cmdline_args(app_render_args)
    cmdline_args_hou = create_cmdline_args(render_args_hou)

    default_log_dir = Path(render_args_hou.out_dir).parent
    logger.info(f"Server created cmdline args: {cmdline_args_hou}")
    # logger.info(f"process.poll(): {process.poll()}")
    # logger.info(f"process.pid: {process.pid}")
    # Submit the hou rendering job
    job_hou = q.enqueue(
        start_subprocess,
        cmdline_args_hou,
        log_dir = default_log_dir,
        job_timeout="6h",
    )

    # submitted_jobs.append(job)
    logger.info("Submitted!")
    logger.info(f"job.result: {job_hou.result}")

    return str(job_hou.result)

