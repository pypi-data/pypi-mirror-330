import logging
from pathlib import Path
from typing import Optional, Union
from uuid import UUID


# from app.project_manager import ProjectManager
# from app.job_manager import JobManager

from . import render_task_local as rtl
from ceon_render.render_job import CeonRenderJob
from ceon_render.file_reference import CeonFileSourceType, CeonFileReference

# from ceon_render.app import CeonRenderAppType

logger = logging.getLogger(__name__)


def render_task(
    ceon_task: CeonRenderJob,
    job_uuid: Union[UUID, str],
) -> rtl.RenderTaskLocal:
    logger.info(f"Converting ceon task: {ceon_task=}")
    chosen_fn = LOOKUP_FN[ceon_task.app_type]
    render_task_local = chosen_fn(ceon_task, job_uuid)
    logger.info(f"Created local render task: {render_task_local=}")
    return render_task_local


def render_task_hou(
    ceon_task: CeonRenderJob, job_uuid: Union[UUID, str]
) -> rtl.RenderTaskLocalHou:
    hipfile = resolve_file_reference(ceon_task.task_input, job_uuid=job_uuid)
    app_render_settings: CeonRenderJobAppSettingsHou = (
        ceon_task.app_render_settings
    )

    # TODO 'apply job frame limit' general-purpose function to handle
    job_frame_limit = _get_job_frame_limit(str(job_uuid))
    if job_frame_limit:
        frames = job_frame_limit
        logger.warning(
            "TODO: Find overlap between job frame limit and task frames"
        )
    else:
        frames = app_render_settings.frames

    dimensions = str(app_render_settings.out_dimensions)
    local_task = rtl.RenderTaskLocalHou(
        hipfile=str(hipfile),
        target_node=app_render_settings.target_node,
        out_filename=ceon_task.task_output,
        out_dimensions=dimensions,
        frames=frames,
    )
    return local_task


# def _get_job_frame_limit(job_uuid: Union[str, UUID]) -> Optional[str]:
#     # Get job frame limit
#     try:
#         job_frame_limit = JobManager(job_uuid).load().limit_frames
#         return job_frame_limit
#     except ceon_errors.CeonInstantiationError as e:
#         logger.warning(
#             f"Could not check job_frame_limit: Failed to load local job {job_uuid}: {e}"
#         )
#         return None


def render_task_ffmpeg(
    ceon_task: CeonRenderJob, job_uuid: Union[UUID, str]
) -> rtl.RenderJobLocalFFMPEG:
    app_render_settings: CeonRenderJobAppSettingsFFMPEG = (
        ceon_task.app_render_settings
    )
    input_file = resolve_file_reference(
        ceon_task.task_input, job_uuid=job_uuid
    )

    # TODO 'apply job frame limit' general-purpose module/function to handle modifications
    job_frame_limit = _get_job_frame_limit(job_uuid)
    if job_frame_limit:
        start_frame = job_frame_limit.split(" ")[0]
        logger.debug(f"Got start frame: {start_frame}")
        logger.warning(
            "TODO: ffmpeg check for -start-number already in args before modifying?"
        )
        # prepend the start_number arg for img sequenes
        logger.warning(
            "TODO: Handle non-image-sequence inputs with a job frame limit?"
        )
        logger.warning(
            "TODO: Handle unknown start_frame number by using a glob pattern instead of start_number (setup when generating the ceon ffmpeg task, NOT here in ceon_to_local.)"
        )
        # https://superuser.com/questions/1671423/ffmpeg-input-image-sequence-can-i-add-arbitrary-list-of-images-to-that
        input_args = (
            f"-start_number {start_frame} {app_render_settings.input_args}"
        )
    else:
        input_args = app_render_settings.input_args
        # Set the start frame on the input.

    local_task = rtl.RenderTaskLocalFFMPEG(
        input_file=str(input_file),
        input_args=input_args,
        output_file=ceon_task.task_output,
        output_args=app_render_settings.output_args,
    )
    return local_task


LOOKUP_FN = {
    CeonRenderAppType.HOU: render_task_hou,
    CeonRenderAppType.FFMPEG: render_task_ffmpeg,
}


def resolve_file_reference(
    ceon_file_reference: CeonFileReference,
    project_uuid: Optional[Union[UUID, str]] = None,
    job_uuid: Optional[Union[UUID, str]] = None,
) -> Path:
    def resolve_file_reference_job_input(target: str) -> Path:
        if not job_uuid:
            raise Exception(
                "Canot resolve file reference for file source from job_input: job_uuid not provided."
            )
        job_inputs_dir = JobManager(job_uuid=job_uuid).paths().job_inputs
        return Path(job_inputs_dir, target)

    def resolve_file_reference_job_output(target: str) -> Path:
        if not job_uuid:
            raise Exception(
                "Canot resolve file reference for file source from job_output: job_uuid not provided."
            )
        job_outputs_dir = JobManager(job_uuid=job_uuid).paths().job_outputs
        return Path(job_outputs_dir, target)

    # def resolve_file_reference_project(target: str) -> Path:
    #     if (not job_uuid) and (not project_uuid):
    #         raise Exception(
    #             "Canot resolve file reference for file source from project: neither job_uuid nor project_uuid provided."
    #         )

    #     if project_uuid:
    #         project_dir = ProjectManager(project_uuid=project_uuid).path()
    #         # logger.info(f"project_uuid not provided. Fetching from project: {project_uuid}")
    #     else:
    #         # Try to fetch the project_uuid from the job
    #         project_uuid_from_job = (
    #             JobManager(job_uuid=str(job_uuid)).load().project_uuid
    #         )
    #         project_dir = ProjectManager(
    #             project_uuid=project_uuid_from_job
    #         ).path()
    #     return Path(project_dir, target)

    lookup_fn = {
        # CeonFileSourceType.PROJECT: resolve_file_reference_project,
        CeonFileSourceType.JOB_INPUT: resolve_file_reference_job_input,
        CeonFileSourceType.JOB_OUTPUT: resolve_file_reference_job_output,
        CeonFileSourceType.ABSOLUTE: lambda x: Path(x),
    }
    chosen_fn = lookup_fn[ceon_file_reference.file_source]
    file_path = chosen_fn(ceon_file_reference.target)
    return file_path.resolve()
