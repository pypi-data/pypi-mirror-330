import logging
import requests
import json
import subprocess
import time
from typing import ClassVar
from abc import ABC
from dataclasses import dataclass, field

from ceon_render.render_provider import (
    RenderProvider,
    RenderProviderAppHandler,
)
from ceon_render.render_provider import RenderProviderConfig
from ceon_render import render_app
from ceon_render import JobProgress

from .app_handlers import RenderProviderLocalBlockingAppHandlerFFmpeg

logger = logging.getLogger(__name__)


@dataclass
class RenderProviderLocalBlockingConfig(RenderProviderConfig): ...


class RenderProviderLocalBlocking(RenderProvider):
    name = "local_blocking"
    app_handlers = {"ffmpeg": RenderProviderLocalBlockingAppHandlerFFmpeg()}
    default_config = RenderProviderLocalBlockingConfig()  # Default config

    def __init__(self):
        pass

    def submit_job(
        self,
        # job_uuid: str,
        app_render_job: render_app.AppRenderJob,
        render_provider_config: (
            RenderProviderLocalBlockingConfig | None
        ) = None,
    ) -> str:
        print("SUBMITING via local_blocking render provider...")
        if not render_provider_config:
            render_provider_config = self.default_config

        # Prepare payload
        app_handler = self.app_handlers[app_render_job.app_type]
        print(f"Got app handler: {app_handler}")

        # Submit to LocalBlocking
        job_id = app_handler.submit_job(
            render_job=app_render_job, render_provider_config=None
        )
        return job_id

    def submit_jobs(
        self,
        app_render_jobs: list[render_app.AppRenderJob],
        render_provider_config: (
            RenderProviderLocalBlockingConfig | None
        ) = None,
    ) -> str:
        """Submit a render job to the provider
        ceon_render_jobs: A list of CeonRenderJob instance containing all information about the render job to be executed.
        render_provider_config: An optional dict config to modify the provider behaviour (example: Frame batch size)

        Return: An id that is used by the provider to track the job progress and download results.
        """
        # TODO handle dependency chaining.
        last_job_id = ""
        for job in app_render_jobs:
            last_job_id = self.submit_job(job, render_provider_config)
        # Returns only the final job in the sequence.
        return last_job_id

    def check_for_job_completion(self, provider_job_id: int | str) -> bool:
        """
        Query local_blocking to check on the job status.
        Return: True if the job is complete, False otherwise.
        Raises an exception if the job failed!
        """
        logger.warning(
            "local_blocking check_for_job_completion() always returns True."
        )
        return True

    # TODO move this into baseclass? It is implementation agnostic assuming that 'check_for_job_completion' exists.
    def wait_for_job_completion(
        self, provider_job_id: str, poll_interval_seconds=30
    ):
        """
        A blocking method that waits for a render to complete.
        provider_job_id: The job_id of the LocalBlocking job.
        poll_interval: The number of seconds between checks
        """
        print(
            f"Waiting for job completion {provider_job_id} (poll={poll_interval_seconds}s)..."
        )
        # job_has_completed = self.check_for_job_completion(provider_job_id)
        while not self.check_for_job_completion(provider_job_id):
            time.sleep(poll_interval_seconds)
            # job_has_comleted = self.check_for_job_completion(provider_job_id)
        print(f"Job {provider_job_id} ended.")
        return

    def download_job_outputs(self, provider_job_id: str | int):
        logger.warning(
            "local_blocking download_job_outputs() always returns received id."
        )
        return provider_job_id
