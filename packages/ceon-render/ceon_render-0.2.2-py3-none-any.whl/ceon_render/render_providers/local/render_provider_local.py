import requests
import json
from typing import ClassVar
from abc import ABC
from dataclasses import dataclass, field

from ceon_render.render_provider import (
    RenderProvider,
    RenderProviderAppHandler,
)

# from ceon_render.render_job import CeonRenderJob
from ceon_render import render_app

# import render_apps

from . import houdini
from . import ffmpeg


class RenderProviderLocal(RenderProvider):
    name = "local"
    app_handlers = {
        "hou": houdini.RenderProviderAppHandlerHou(),
        "ffmpeg": ffmpeg.RenderProviderAppHandlerFFmpeg(),
    }

    def __init__(self, api_url):
        self.api_url = api_url

    def submit_job(
        self,
        # job_uuid: str,
        app_render_job: render_app.AppRenderJob,
        render_provider_config: dict | None = None,
    ) -> str:
        """Submit a job.
        Returns: The provider ID for the submitted job."""
        print("SUBMITING via local render provider...")

        # Convert to app render job instances
        print(f"Local server: {self.api_url}")
        try:
            app_handler: RenderProviderAppHandler = self.app_handlers[
                app_render_job.app_type
            ]
        except KeyError:
            # Todo add UnsupportedAppError exceiption to ceon_render module
            raise Exception(
                f"Unsupported app type '{app_render_job.app_type}' for provider '{self.__class__.__name__}'"
            )
        # local_render_job = app_handler.ceon_to_local(ceon_render_job)
        print(f"Got app handler: {app_handler}")
        payload = app_handler.create_payload(app_render_job)
        app_endpoint = app_handler.endpoint(self.api_url)
        res = _post_request(app_endpoint, payload)
        provider_job_id = res.json()
        return provider_job_id

    def submit_jobs(
        self,
        app_render_jobs: list[render_app.AppRenderJob],
        render_provider_config: dict | None = None,
    ):
        """
        Submit multiple render jobs to the render server to be submitted as a group.
        Returns: ???
        """
        print(f"Received render jobs: {app_render_jobs}")
        print(f"Local server: {self.api_url}")
        print("Preparing pipeline submission for local rendering server ...")
        # log_dir = f"{JobPaths(job_uuid).logs}/local_rendering"
        log_dir = "/mnt/FileStorage/Dayne/tmp"

        payload_jobs = []
        for app_render_job in app_render_jobs:
            app_handler = self.app_handlers[app_render_job.app_type]
            # local_render_job = app_handler.ceon_to_local(render_job)
            payload = app_handler.create_payload(app_render_job)
            pipeline_payload_job = {
                "app": app_render_job.app_type,
                "payload": payload,
            }
            payload_jobs.append(pipeline_payload_job)
        payload = {"render_tasks": payload_jobs, "log_dir": log_dir}

        endpoint = f"{self.api_url}/render/pipeline"
        res = _post_request(endpoint, payload)
        res_json = res.json()
        return res_json

    def check_for_job_completion(self, provider_job_id: int | str) -> bool:
        """
        Return: True if the job is complete, False otherwise.
        Raises an exception if the job failed!
        """
        url = f"{self.api_url}/job/{provider_job_id}"
        res = requests.get(url, json={})
        print(f"Got res : {res}")
        res_json = res.json()
        print(f"Got res json {res_json}")
        status = res_json["job_status"]
        if status == "finished":
            return True
        if status == "failed":
            raise Exception(
                f"Conductor job failed (TODO custom exception for handling): {provider_job_id}"
            )
        # Assume the job is unstarted or running.
        # TODO handle sates better (Allow server to return 'finished', 'success' boolean properties so that
        # local rendering server can handle it's own internal logic.)
        return False

    # TODO return downloaded files?
    def download_job_outputs(self, provider_job_id: str | int):
        return


def _post_request(url, payload):
    print(f"Posting request to: {url}")
    print(f"payload: {json.dumps(payload, indent=2)}")
    res = requests.post(url, json=payload)
    print(f"Got res: {res}")
    if res.ok:
        print(f"Got res.json(): {res.json()}")
        return res
    else:
        print(f"Failed to submit render. res: {res}")
        raise Exception(f"Got not-ok response ffrom render server: {res}")
