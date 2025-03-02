# Provider agnostic classes that store all relevant args required to execute
# a job for a particular app type.

# To make the app args available for providers to consume, these classes should
# be registered via the ceon_render.render_app.register()
# E.g. ceon_render.render_app.register(AppRenderJobHou)
from dataclasses import dataclass, field
from typing import ClassVar, Self, Type
from enum import StrEnum, auto

from ceon_render.render_app import AppRenderJob
from ceon_render.render_pipeline import (
    CeonRenderPipeline,
    CeonRenderPipelineJob,
)
from ceon_render.file_reference import resolve_file_reference
from ceon_render.render_settings import CeonRenderJobSettings

# from ceon_render.render_pipeline import CeonRenderPipelineJob


class HoudiniRenderType(StrEnum):
    KARMA_CPU = auto()
    KARMA_GPU = auto()
    REDSHIFT = auto()
    SIM = auto()


@dataclass
class AppRenderArgsHou:
    """Contains a list of expected args which should be present in  the 'app_render_settings' property
    of a pipeline job."""

    target_node: str
    node_type: HoudiniRenderType
    frames: str


@dataclass
class AppRenderJobHou(AppRenderJob):
    """Contains all args required to execute a single houdini render.
    This is the job definition that can be passed to any provider which supports Houdini.
    Individual render providers may require only subsets of this information.
    """

    app_type: ClassVar[str] = "hou"

    hipfile: str  # Path to the hipfile
    target_node: str  # The ROP node inside the hipfile
    node_type: HoudiniRenderType
    output_file: str  # Can include houdini vars e.g. $HIP, $F4
    frame_range: tuple[int, int, int]  # start, end, inc
    frame_dimensions: tuple[int, int]  # width, height
    env: dict[str, str] = field(
        default_factory=dict
    )  # [ENV_TO_SET=Value, ANOTHER=Val2]
    job_name: str = "unnamed_hou_job"

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
        app_render_settings = AppRenderArgsHou(
            **pipeline_job.app_render_settings
        )

        if not render_settings.frame_dimensions:
            raise Exception(
                f"Cannot create a concrete job of type {cls.app_type} because received render_settings do not contain frame dimensions: {render_settings=}"
            )

        # if not render_settings.frame_range:
        #     raise Exception(
        #         f"Cannot create a concrete job of type {cls.app_type} because received render_settings do not contain a frame range: {render_settings=}"
        #     )

        # TODO use tuple in app_render_settings instead of coercing format here.
        frames_split = app_render_settings.frames.split(" ")
        frames = (int(frames_split[0]), int(frames_split[1]), 1)
        if render_settings.frame_range:
            frames = render_settings.frame_range
        return cls(
            hipfile=job_input,
            target_node=app_render_settings.target_node,
            node_type=app_render_settings.node_type,
            output_file=job_output,
            frame_range=frames,
            frame_dimensions=render_settings.frame_dimensions,
            env=render_settings.env,
            job_name=pipeline_job.job_name,
        )
