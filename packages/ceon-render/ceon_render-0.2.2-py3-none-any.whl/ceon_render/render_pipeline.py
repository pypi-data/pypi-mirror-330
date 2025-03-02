from typing import TypedDict
from uuid import uuid4
from dataclasses import dataclass, field, asdict

from ceon_render.render_app import AppRenderJob, get_app_job_cls
from ceon_render import render_provider
from ceon_render.render_settings import CeonRenderJobSettings
from ceon_render import render_provider as rp

from .file_reference import CeonFileReference
from .file_reference import resolve_file_reference


@dataclass(kw_only=True)
class CeonRenderPipelineJob:
    """
    Defines a job to be run as part of a pipeline.
    Stores only the logistical information relevant to the pipeline (target app/node/file to render, ffmpeg cmd to execute etc)
    It is agnostic of specific render settings/implementtions such as resolution, frame ranges, batch size etc.
    """

    job_name: str  # Human readable identifier for this job.
    app_type: str
    app_version: str
    app_render_settings: dict  # Args required for this particular app_type

    job_input: CeonFileReference  # Input file
    job_output: str  # Output file

    # Store other render jobs which must be completed before this one can start
    job_dependencies: list[str] = field(default_factory=list)
    job_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        if not isinstance(self.job_input, CeonFileReference):
            raise ValueError("job_input must be a CeonFileReference type")

    def __str__(self):
        msg = f"<{self.__class__.__name__} '{self.job_name}' ({self.app_type} OUT:'{self.job_output}')>"
        return msg

    def __repr__(self):
        return self.__str__()


@dataclass
class CeonRenderPipeline:
    """
    output_job: The name of the pipeline_job output to be passed back to the user.
    output_extras: An optional list of additional task names whose outputs will also be passed back to the user.
    """

    pipeline_jobs: list[CeonRenderPipelineJob]
    output_job: str
    output_extras: list[str] = field(default_factory=list)
    # output_extras: list[CeonRenderPipelineExtraOutput] = field(default_factory=list)

    def get_job(self, pipeline_job_name: str):
        """Return the CeonRenderPipelineJob instance with the matching name.
        Raise an exception if not found."""
        for job in self.pipeline_jobs:
            if job.job_name == pipeline_job_name:
                return job
        raise Exception(
            f"Could not find job in pipeline for pipeline_job_name: {pipeline_job_name}: {self=}"
        )

    def __str__(self):
        job_names = [
            pipeline_job.job_name for pipeline_job in self.pipeline_jobs
        ]
        msg = f"<{self.__class__.__name__} jobS:{job_names} OUT:'{self.output_job}')>"
        return msg

    def __repr__(self):
        return self.__str__()


def pipeline_to_concrete_jobs(
    pipeline: CeonRenderPipeline,
    *,
    file_reference_dirs: dict[str, str],
    render_settings: CeonRenderJobSettings,
) -> list[AppRenderJob]:
    """Convert a pipeline into a set of concrete AppRenderJob instances
    dirs: Dict mapping key(FileReferenceType) to root directories
    """
    # TODO setup as function in ceon_render module.
    print(f"Creating concrete task instances from pipeline: {pipeline=}")
    print(f"{pipeline.pipeline_jobs=}")
    concrete_jobs = []
    # TODO list comprehension after refactoring is complete and confirmed to work
    for pipeline_job in pipeline.pipeline_jobs:
        concrete_job = pipeline_job_to_concrete_job(
            pipeline,
            pipeline_job,
            file_reference_dirs=file_reference_dirs,
            render_settings=render_settings,
        )
        print(f"Created concrete job: {concrete_job}")
        concrete_jobs.append(concrete_job)
    print(f"Returning concrete jobs: {concrete_jobs}")
    return concrete_jobs
    # instances = [pipeline_job_to_concrete_job(pipeline, job, file_reference_dirs=file_reference_dirs)]
    # app_cls = get_app_job_cls(pipeline_task.app_type)
    # pipeline_task_args = asdict(pipeline_task)

    # # Replace file references
    # input_file_reference = pipeline_task_args["job_input"]
    # input = _resolve_file_reference(
    #     input_file_reference, file_reference_dirs=file_reference_dirs
    # )
    # output_file_reference = pipeline_task_args["job_output"]
    # output = _resolve_file_reference(
    #     output_file_reference, file_reference_dirs=file_reference_dirs
    # )

    # instance = app_cls(**asdict(pipeline_task))
    # print(f"Created concrete task instance: {instance=}")
    # return instance


def pipeline_job_to_concrete_job(
    pipeline: CeonRenderPipeline,
    pipeline_job: CeonRenderPipelineJob,
    *,
    render_settings: CeonRenderJobSettings,
    file_reference_dirs: dict[str, str],
) -> AppRenderJob:
    """Convert a pipeline into a set of concrete AppRenderJob instances
    dirs: Dict mapping key(FileReferenceType) to root directories
    """
    # TODO setup as function in ceon_render module.
    print(
        f"Creating concrete task instance from pipeline task: {pipeline_job=}"
    )

    # Replace file_reference with resolved filepaths
    app_cls = get_app_job_cls(pipeline_job.app_type)
    instance = app_cls.from_pipeline_job(
        pipeline_job=pipeline_job,
        pipeline=pipeline,
        file_reference_dirs=file_reference_dirs,
        render_settings=render_settings,
    )
    print(f"Created concrete task instance: {instance=}")
    return instance


# TODO types dict?
class CeonRenderJobGroup(TypedDict):
    render_provider: str
    job_names: list[str]  # A list of job_names to submit


def group_jobs_by_render_provider(
    jobs: list[AppRenderJob],
    allowed_providers: list[str] | None = None,
) -> list[CeonRenderJobGroup]:
    """Receives a list of pipeline jobs and returns grouped tasks along with
    which render provider they should be submitted to.
    allowed_providers: The providers to search for. If None, uses all registered providrs.
    The first item in the list takes priority and is considered the preferd provider.
    TODO: Handle dependency graphing.
    """
    # TODO handle dependency managements.
    print(f"Building render job groups by supported providers")
    if allowed_providers is None:
        allowed_providers = render_provider.list_providers()
    print(f"{allowed_providers=}")

    # Find a provider for the first task in the list.
    first_job = jobs[0]

    # Init for looping logic
    current_provider_name = _choose_provider_for_app_type(
        first_job.app_type, available_providers=allowed_providers
    )
    job_groups = []
    current_group: CeonRenderJobGroup = {
        "render_provider": current_provider_name,
        "job_names": [first_job.job_name],
    }
    # TODO add job_name to AppRenderJob for clearer identifications
    # and linking with associated pipeline jobs.
    print(f"first job ({first_job.app_type}){current_provider_name=}")
    # Use the same provider for as many of the subsequent tasks as possible
    # If a task is encountered that is not supported by the current providers,
    # switch to the next-best(preferred) available provider
    for job in jobs[1:]:
        chosen_provider = _choose_provider_for_app_type(
            job.app_type, available_providers=allowed_providers
        )
        print(f"job ({job.app_type}){chosen_provider=}")

        # If the prefered provider changes, start a new group
        if chosen_provider != current_provider_name:
            job_groups.append(current_group.copy())
            current_group = {
                "render_provider": chosen_provider,
                "job_names": [job.job_name],
            }
        else:
            current_group["job_names"].append(job.job_name)
    job_groups.append(current_group)
    return job_groups


# TODO merge pipeline_jobs and concrete jobs functions.
# Convert boht (either pipeline or concrete) into dict of job_name, app_type
# and then use reusable logic to generate the output
def group_pipeline_jobs_by_render_provider(
    jobs: list[CeonRenderPipelineJob],
    allowed_providers: list[str] | None = None,
) -> list[CeonRenderJobGroup]:
    """Receives a list of pipeline jobs and returns grouped tasks along with
    which render provider they should be submitted to.
    allowed_providers: The providers to search for. If None, uses all registered providrs.
    The first item in the list takes priority and is considered the preferd provider.
    TODO: Handle dependency graphing.
    """
    # TODO handle dependency managements.
    print(f"Building render job groups by supported providers")
    if allowed_providers is None:
        allowed_providers = render_provider.list_providers()
    print(f"{allowed_providers=}")

    # Find a provider for the first task in the list.
    first_job = jobs[0]

    # Init for looping logic
    current_provider_name = _choose_provider_for_app_type(
        first_job.app_type, available_providers=allowed_providers
    )
    job_groups = []
    current_group: CeonRenderJobGroup = {
        "render_provider": current_provider_name,
        "job_names": [first_job.job_name],
    }
    # TODO add job_name to AppRenderJob for clearer identifications
    # and linking with associated pipeline jobs.
    print(f"first job ({first_job.app_type}){current_provider_name=}")
    # Use the same provider for as many of the subsequent tasks as possible
    # If a task is encountered that is not supported by the current providers,
    # switch to the next-best(preferred) available provider
    for job in jobs[1:]:
        chosen_provider = _choose_provider_for_app_type(
            job.app_type, available_providers=allowed_providers
        )
        print(f"job ({job.app_type}){chosen_provider=}")

        # If the prefered provider changes, start a new group
        if chosen_provider != current_provider_name:
            job_groups.append(current_group.copy())
            current_group = {
                "render_provider": chosen_provider,
                "job_names": [job.job_name],
            }
        else:
            current_group["job_names"].append(job.job_name)
    job_groups.append(current_group)
    return job_groups


# def group_pipeline_jobs_by_render_provider(
#     pipeline_jobs: list[CeonRenderPipelineJob],
#     allowed_providers: list[str] | None = None,
# ) -> list[CeonRenderPipelineJobGroup]:
#     """Receives a list of pipeline jobs and returns grouped tasks along with
#     which render provider they should be submitted to.
#     allowed_providers: The providers to search for. If None, uses all registered providrs.
#     The first item in the list takes priority and is considered the preferd provider.
#     TODO: Handle dependency graphing.
#     """
#     # TODO handle dependency managements.
#     print(f"Building render job groups by supported providers")
#     if allowed_providers is None:
#         allowed_providers = render_provider.list_providers()
#     print(f"{allowed_providers=}")

#     # Find a provider for the first task in the list.
#     first_job = pipeline_jobs[0]

#     # Init for looping logic
#     current_provider_name = _choose_provider_for_app_type(
#         first_job.app_type, available_providers=allowed_providers
#     )
#     job_groups = []
#     current_group: CeonRenderPipelineJobGroup = {
#         "render_provider": current_provider_name,
#         "pipeline_jobs": [first_job],
#     }
#     print(
#         f"first job {first_job.job_name} ({first_job.app_type}){current_provider_name=}"
#     )
#     # Use the same provider for as many of the subsequent tasks as possible
#     # If a task is encountered that is not supported by the current providers,
#     # switch to the next-best(preferred) available provider
#     for job in pipeline_jobs[1:]:
#         chosen_provider = _choose_provider_for_app_type(
#             job.app_type, available_providers=allowed_providers
#         )
#         print(f"job {job.job_name} ({job.app_type}){chosen_provider=}")

#         # If the prefered provider changes, start a new group
#         if chosen_provider != current_provider_name:
#             job_groups.append(current_group.copy)
#             current_group = {
#                 "render_provider": chosen_provider,
#                 "pipeline_jobs": [job],
#             }
#         else:
#             current_group["pipeline_jobs"].append(job)
#     job_groups.append(current_group)

#     print("Created job groups:")
#     print(job_groups)
#     return job_groups


def _create_task_chain_for_provider(
    pipeline_jobs: list[CeonRenderPipelineJob], provider_name: str
):
    """Iterate through the jobs until one is found which is not supported by the current
    provider.
    Returns: the index of the unsupported app_type
    """
    # Useful for building more ocmplex selection strategies
    ...


def _choose_provider_for_app_type(
    app_type: str, available_providers: list[str]
):
    """
    app_type: The app type to choose a provider for.
    available_providers: An ordered list of strings where the first item is the
        preferred render provider
    """
    for provider_name in available_providers:
        provider = rp.get(provider_name)
        if app_type in provider.supported_apps():
            return provider_name
    raise Exception(
        f"Could not find a render provider for app_type: {app_type}"
    )


def _find_supported_providers_for_all_tasks(
    cstock_render_tasks: list[CeonRenderPipelineJob],
) -> list[str]:
    """
    Returns a list of render providers which are valid for ALL tasks in the list.
    Return an empty list if no common providers are found.
    """
    if not cstock_render_tasks:
        raise Exception(
            f"find_common_providers received an invalid argument for cstock_render_tasks: {cstock_render_tasks}"
        )

    task_app_types = [task.app_type for task in cstock_render_tasks]
    # lists_of_providers = [
    #     LOOKUP_PROVIDERS_FOR_APP[app_type] for app_type in task_app_types
    # ]

    # All known providers
    available_providers = set(
        [provider_name for provider_name in rp.list_providers()]
    )
    if not available_providers:
        raise Exception(
            "Cannot submit render: No registered render providers found."
        )

    # Providers after filtering by app
    valid_providers = available_providers.copy()

    # Filter by removing any providers which don't support all of the required app_types
    for provider_name, provider in rp.render_providers.items():
        provider_apps = provider.supported_apps()
        # logger.warning("")
        for task_app_type in task_app_types:
            if task_app_type not in provider_apps:
                valid_providers.discard(provider_name)
                continue

    return list(valid_providers)


# def _resolve_file_reference(
#     file_reference: CeonFileReference | str,
#     file_reference_dirs: dict[str, str],
# ) -> str:
#     """
#     Resolve a file reference by converting it to an absolute file path
#     If the file_reference is str it is assumed to belong to a job_output
#     file_reference_dirs: Maps keys to the target root directory
#     """
#     # All job_input paths should be CeonFileReference instances
#     print(f"Resolving file_reference: {file_reference=}")

#     # A received str type is assumed to be a job_output.
#     if isinstance(file_reference, str):
#         full_path = f"{file_reference_dirs['job_output']}/{file_reference}"
#         return full_path

#     # Assumed to be ajob_input
#     # Uses the file_reference source type to fetch the path.
#     root_dir = file_reference_dirs[file_reference.file_source.value]
#     full_path = f"{root_dir}/{file_reference.target}"
#     return full_path
