from pathlib import Path

from ceon_render import render_provider
from ceon_render.render_apps import AppRenderJobFFmpeg
from ceon_render.render_provider import RenderProviderAppHandler

from . import execute


class RenderProviderLocalBlockingAppHandlerFFmpeg(RenderProviderAppHandler):
    def __init__(self):
        pass

    def submit_job(
        self,
        render_job: AppRenderJobFFmpeg,
        render_provider_config: "RenderProviderLocalBlockingConfig",
    ) -> str:
        print("Submitting local render ffmpeg job to local_blocking...")
        # Contains uploads for the job (project dir)
        # upload_paths = render_provider_config.upload_paths

        input_args_list = render_job.input_args.split()
        output_args_list = render_job.output_args.split()
        output_file = render_job.output_file
        # temp_file = get_temp_file(task_args)

        # A temporary filename is used while writing so that the 'final' file can't be mistakenly
        # detected as existing while the rendering is still incomplete.
        cmd_to_run = [
            "ffmpeg",
            *input_args_list,
            "-i",
            render_job.input_file,
            *output_args_list,
            output_file,
        ]
        # TODO move log_dir to render_provider_config
        log_dir = Path(output_file).resolve().absolute().parent
        result = execute.start_subprocess(
            cmd_to_run, log_dir=str(log_dir), wait=True
        )
        return str(result.pid)
