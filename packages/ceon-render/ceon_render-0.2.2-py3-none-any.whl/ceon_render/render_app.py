from abc import ABC
from dataclasses import dataclass, field
from typing import Protocol
from typing import Callable
from typing import Type
from typing import ClassVar

from ceon_render.render_settings import CeonRenderJobSettings

# from ceon_render.render_pipeline import CeonRenderPipelineJob
# from ceon_render.render_pipeline import CeonRenderPipeline


# Base class for creating classes which store all args required to execute
# a rendering job for a particular app.
# This is provider agnostic, will be passed to and handled by the providers.
@dataclass(kw_only=True)
class AppRenderJob(ABC):
    app_type: ClassVar[str]  # The name used to identify this app.
    file_dependencies: list[str] = field(default_factory=list)

    @classmethod
    def from_pipeline_job(
        cls,
        pipeline_job: "CeonRenderPipelineJob",
        file_reference_dirs: dict,
        render_settings: "CeonRenderJobSettings",
        pipeline: "CeonRenderPipeline | None" = None,
    ) -> "AppRenderJob":
        """Create an AppRenderJob from a pipeline job.
        pipeline: The full pipeline, required if a pipeline job references another task
        in the pipeline.
        file_reference_dirs: A dictionary of paths which must be passed to resolve
        pipeline CeonFileReference instances into absolute file paths.
        Returns: The AppRenderJob instance of the appropriate app type."""
        ...


render_apps: dict[str, Type[AppRenderJob]] = {}


# EXAMPLE usage with dataclasses syntax to support rendering jobs in Houdini:
# class AppRenderJobHou(AppRenderJob):
#     app_type: ClassVar[str] = "hou"

#     hipfile: str
#     target_node: str
#     ...

# would contain all args required to execute a houdini render, regardless of provider used.


def register(app_render_settings_class: Type):
    """Register a new render app"""
    app_name = app_render_settings_class.app_type
    if app_name in render_apps.keys():
        raise ValueError(
            f"Cannot register render app because a app with name '{app_name}' already exists"
        )
    render_apps[app_name] = app_render_settings_class


def unregister(render_app_name: str):
    """Unregister a render app"""
    render_apps.pop(render_app_name, None)


def get_app_job_cls(render_app_name: str) -> Type[AppRenderJob]:
    """Fetch a render app by their registered name"""
    return render_apps[render_app_name]
