from dataclasses import dataclass
from typing import ClassVar, Self

from ceon_render.render_settings import CeonRenderJobSettings
from ceon_render.file_reference import resolve_file_reference
from ceon_render.render_app import AppRenderJob


@dataclass
class AppRenderArgsFFmpeg:
    input_args: str = ""
    output_args: str = ""


@dataclass
class AppRenderJobFFmpeg(AppRenderJob):
    """Contains all information to build an ffmpeg command"""

    app_type: ClassVar[str] = "ffmpeg"

    input_file: str
    output_file: str
    input_args: str = ""
    output_args: str = ""
    job_name: str = "unnamed_ffmpeg_job"

    @classmethod
    def from_pipeline_job(
        cls,
        pipeline_job: "CeonRenderPipelineJob",
        file_reference_dirs: dict,
        render_settings: CeonRenderJobSettings,
        pipeline: "CeonRenderPipeline",
    ) -> Self:
        job_input = resolve_file_reference(
            pipeline_job.job_input, file_reference_dirs
        )
        job_output = resolve_file_reference(
            pipeline_job.job_output, file_reference_dirs
        )
        # Instantiate to validate received app args
        app_render_settings = AppRenderArgsFFmpeg(
            **pipeline_job.app_render_settings
        )
        return cls(
            input_file=job_input,
            input_args=app_render_settings.input_args,
            output_file=job_output,
            output_args=app_render_settings.output_args,
            job_name=pipeline_job.job_name,
        )
