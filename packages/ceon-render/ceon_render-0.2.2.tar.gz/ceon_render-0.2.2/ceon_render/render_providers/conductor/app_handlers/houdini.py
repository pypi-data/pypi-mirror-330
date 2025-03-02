from pathlib import Path

from ceon_render import render_provider
from ceon_render.render_apps import AppRenderJobHou
from ceon_render.render_provider import RenderProviderAppHandler

from .conductor_payload import create_payload

DEFAULT_HYTHON_SCRIPT = str(
    Path(Path(__file__).parent, "hython_render.py").resolve().absolute()
)


class RenderProviderConductorAppHandlerHou(RenderProviderAppHandler):
    def __init__(self, hython_script: str | None = None):
        self.hython_script_path = (
            hython_script if hython_script else DEFAULT_HYTHON_SCRIPT
        )
        if not Path(self.hython_script_path).exists():
            raise Exception(
                f"File not found: Hython script required for Conductor houdini app handler. Missing file: {self.hython_script_path}"
            )

    def create_payload(
        self,
        hou_render_job: AppRenderJobHou,
        render_provider_config: "RenderProviderConductorConfig",
    ) -> dict:
        print("Submitting local render hou job to conductor...")
        # Contains uploads for the job (project dir)
        # upload_paths = render_provider_config.upload_paths
        upload_paths = hou_render_job.file_dependencies
        upload_paths.append(
            self.hython_script_path,
        )
        job_title = (
            render_provider_config.job_title
            if render_provider_config.job_title
            else "Untitled job"
        )
        # TODO fetch environment for appropriate houdini version!
        # Environment can be fetched with ciocore api_client.request_software_packages()
        # Filter for the appropriate version and extract the environment.
        payload = create_payload(
            job_title=job_title,
            project="api_testing",
            script_filepath=self.hython_script_path,
            scene_filepath=hou_render_job.hipfile,
            driver=hou_render_job.target_node,
            frames=hou_render_job.frame_range,
            resolution=hou_render_job.frame_dimensions,
            vars=hou_render_job.env,
            upload_paths=upload_paths,
            output_path=hou_render_job.output_file,
            batch_size=render_provider_config.batch_size,
        )
        return payload.as_dict()

    def endpoint(self, api_url: str):
        """Return the endpoint for submitting a job fo this particular app type"""
        return f"{api_url}/render/hou"
