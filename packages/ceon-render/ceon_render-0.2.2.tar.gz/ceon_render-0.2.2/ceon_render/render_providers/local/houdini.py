import logging
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
from typing import ClassVar
from uuid import UUID

from ceon_render.render_apps import AppRenderJobHou
from ceon_render.render_provider import RenderProviderAppHandler

logger = logging.getLogger(__name__)


class RenderProviderAppHandlerHou(RenderProviderAppHandler):
    def __init__(self, config: dict | None = None):
        self.config = config if config else {}

    def create_payload(self, hou_render_job: AppRenderJobHou) -> dict:
        print("Submitting local render ffmpeg job (mock)...")
        # Convert generic app type to type expected by provider
        payload = create_payload(hou_render_job)
        return payload

    def endpoint(self, api_url: str):
        """Return the endpoint for submitting a job fo this particular app type"""
        return f"{api_url}/render/hou"


def _env_dict_to_list(dict_env: dict[str, str]):
    """Convert from dict format to the list format expected by the render server"""
    return [f"{key}={value}" for key, value in dict_env.items()]


def create_payload(
    render_task_hou: AppRenderJobHou,
):
    logger.debug("Creating payload for local render task: houdini")
    logger.debug(f"Setting up envs for local hou rendering request...")
    out_dir = str(Path(render_task_hou.output_file).parent)
    out_filename = str(Path(render_task_hou.output_file).name)
    env_list = _env_dict_to_list(render_task_hou.env)
    payload = {
        # "app": task_to_execute.app_type.value,
        "hipfile": f"{render_task_hou.hipfile}",
        "target_node": render_task_hou.target_node,
        "out_dir": str(out_dir),
        "out_filename": out_filename,
        "out_dimensions": "x".join(
            [str(i) for i in render_task_hou.frame_dimensions]
        ),
        "frames": " ".join(str(i) for i in render_task_hou.frame_range),
        "env": env_list,
    }
    return payload
