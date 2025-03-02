import logging
import os
from pathlib import Path
from typing import Union, Dict
from uuid import UUID

from ceon_render.render_provider import RenderProviderAppHandler
from ceon_render.render_apps.ffmpeg import AppRenderJobFFmpeg

logger = logging.getLogger(__name__)


class RenderProviderAppHandlerFFmpeg(RenderProviderAppHandler):
    def __init__(self, config: dict | None = None):
        self.config = config if config else {}

    def create_payload(self, ffmpeg_render_job: AppRenderJobFFmpeg) -> dict:
        print("Submitting local render ffmpeg job...")
        logger.debug("Creating payload for local render task: ffmpeg")

        in_file = ffmpeg_render_job.input_file
        out_file = ffmpeg_render_job.output_file
        input_args = ffmpeg_render_job.input_args
        output_args = ffmpeg_render_job.output_args

        # Load defaults if no args provided
        if not input_args:
            in_ext = Path(in_file).suffix
            input_args = input_args_for_extension(in_ext)
            logger.warning(
                f"No input_args provided for input file: {in_file}, using defaults: {input_args}"
            )
        if not output_args:
            out_ext = Path(out_file).suffix
            output_args = output_args_for_extension(out_ext)
            logger.warning(
                f"No output_args provided for output file: {out_file}, using defaults: {output_args}"
            )

        payload = {
            "input_file": in_file,
            "input_args": input_args,
            "output_file": out_file,
            "output_args": output_args,
        }
        return payload

    def endpoint(self, api_url: str):
        """Return the endpoint for submitting a job fo this particular app type"""
        return f"{api_url}/render/ffmpeg"


def input_args_for_extension(file_extension: str):
    if file_extension.startswith("."):
        # Trim the leading .
        file_extension = file_extension[1:]
    lookup = {
        "tiff": "",  # video to seq
        "mp4": "",  # seq to vid
        "mov": "",
        "exr": "-gamma 2.2",
        "webm": "",
    }
    return lookup[file_extension]


def output_args_for_extension(file_extension: str):
    if file_extension.startswith("."):
        # Trim the leading .
        file_extension = file_extension[1:]
    lookup = {
        "tiff": "-compression_algo raw -pix_fmt rgb24",
        "mp4": "-vcodec libx264 -crf 18  -pix_fmt yuv420p",
        # "mov": "-c:v prores_ks -profile:v 4",
        "mov": "",
        "mkv": "-c:v libvpx-vp9 -row-mt 1 -threads 8",
        "webm": "-c:v libvpx-vp9 -row-mt 1 -threads 8 -b:v 0 -crf 32",
    }
    return lookup[file_extension]
