import time
from typing import Protocol
from typing import Callable
from ceon_render.render_app import AppRenderJob

# from ceon_render.render_job import CeonRenderJob


class RenderProviderConfig(Protocol):
    """
    Stores configuration settings for the render provider, such as batch_size or instance type.
    """

    ...


class RenderProviderAppHandler(Protocol):
    """Handles preparing and submitting a job for a particular app"""

    def submit_job(
        self,
        render_job: AppRenderJob,
        render_provider_config: RenderProviderConfig,
    ) -> str:
        """
        Handles a single job submission for a particular app type.
        Returns: A job_id that can be used to track the progress of the job and download the results.
        """
        ...


class RenderProvider(Protocol):
    """
    Handles submitting, tracking and downloading of render jobs to a particular provider.
    """

    name: str
    app_handlers: dict[str, RenderProviderAppHandler]

    def submit_job(
        self,
        app_render_job: AppRenderJob,
        render_provider_config: RenderProviderConfig | None = None,
    ) -> str:
        """Submit a render job to the provider
        ceon_render_job: A CeonRenderJob instance containing all information about the render job to be executed.
        render_provider_config: An optional dict config to modify the provider behaviour (example: Frame batch size)

        Return: An id that is used by the provider to track the job progress and download results.
        """
        raise NotImplementedError(
            f"submit_job() not implemented for render provider {self.name}"
        )

    def submit_jobs(
        self,
        app_render_jobs: list[AppRenderJob],
        render_provider_config: RenderProviderConfig | None = None,
    ) -> str:
        """Submit a render job to the provider
        ceon_render_jobs: A list of CeonRenderJob instance containing all information about the render job to be executed.
        render_provider_config: An optional dict config to modify the provider behaviour (example: Frame batch size)

        Return: An id that is used by the provider to track the job progress and download results.
        """
        raise NotImplementedError(
            f"submit_jobs() not implemented for render provider {self.name}"
        )

    def check_for_job_completion(self, provider_job_id: str) -> bool:
        """
        Returns:
        - True if the job completed successfully
        - False if the job is in progress.
        - Raise a custom error if the job failed.
        """
        raise NotImplementedError(
            f"check_for_job_completion() not implemented for render provider {self.name}"
        )

    def wait_for_job_completion(
        self, provider_job_id: str, poll_interval_seconds=30
    ):
        """
        A blocking method that waits for a render to complete.
        provider_job_id: The provider_job_id of the job to check for.
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

    def download_job_outputs(self, provider_job_id: str):
        """Download the output files for the target job_id"""
        raise NotImplementedError(
            f"download_job_outputs() not implemented for render provider {self.name}"
        )

    def register_app_handler(
        self, app_name: str, app_handler: RenderProviderAppHandler
    ):
        if app_name in self.app_handlers.keys():
            raise KeyError(
                f"Cannot register app_handler in {self.__class__.__name__} because app '{app_name}' already has a registered handler."
            )
        self.app_handlers[app_name] = app_handler

    def supported_apps(self) -> list[str]:
        """Return: A list of strings which are the names of the supported app types"""
        return list(self.app_handlers.keys())

    # def upload():
    #     """Upload files to the provider's storage"""


render_providers: dict[str, RenderProvider] = {}


def register(render_provider: RenderProvider):
    """Register a new render provider"""
    if render_provider.name in render_providers.keys():
        raise ValueError(
            f"Cannot register render provider because a provider with name '{render_provider.name}' already exists"
        )
    render_providers[render_provider.name] = render_provider


def unregister(render_provider_name: str):
    """Unregister a render provider"""
    render_providers.pop(render_provider_name, None)


# TODO deprecate in favor of get_render_provider
def get(render_provider_name: str) -> RenderProvider:
    """Fetch a render provider by their registered name"""
    return render_providers[render_provider_name]


def get_render_provider(render_provider_name: str) -> RenderProvider:
    """Fetch a render provider by their registered name"""
    return render_providers[render_provider_name]


def list_providers() -> list[str]:
    return list(render_providers.keys())
