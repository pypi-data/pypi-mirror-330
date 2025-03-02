from dataclasses import dataclass

# from enum import StrEnum, auto
from enum import Enum


class CeonFileSourceType(str, Enum):
    """Describes where the target file should be found.
    PROJECT: File path relative to the CEON project dir.
    JOB_INPUT: File path relative to the job inputs dir.
    JOB_OUTPUT: File path relative to the job outputs dir.
    TASK_INPUT: Target is a task name. Resolve the input file of the targeted task.
    TASK_OUTPUT: Target is a task name. Resolve the output file of the targeted task.
    ABSOLUTE: An absolute file path that points to a file on disk.
    """

    PROJECT = "project"
    JOB_INPUT = "job_input"
    JOB_OUTPUT = "job_output"
    TASK_INPUT = "task_input"
    TASK_OUTPUT = "task_output"
    ABSOLUTE = "absolute"


@dataclass
class CeonFileReference:
    """
    Contains the information used to identify a target file.
    target: The value of the file to look for. This could be a file path or a task name depending on the file_source type.
    file_source: A CeonFileSourceType enum describing where to search for the file. This allows lookup of files based on
    job or task inputs/outputs.
    """

    target: str
    file_source: CeonFileSourceType = CeonFileSourceType.PROJECT


def resolve_file_reference(
    file_reference: CeonFileReference | str,
    file_reference_dirs: dict[str, str],
) -> str:
    """
    Resolve a file reference by converting it to an absolute file path.
    If the file_reference is str it is assumed to belong to a job_output
    file_reference_dirs: Maps keys to the target root directory
    """
    # All job_input paths should be CeonFileReference instances
    print(f"Resolving file_reference: {file_reference=}")

    # A received str type is assumed to be a job_output.
    if isinstance(file_reference, str):
        full_path = f"{file_reference_dirs['job_output']}/{file_reference}"
        return full_path

    # Absolute types do not need to make any changes to the path.
    if file_reference.file_source is CeonFileSourceType.ABSOLUTE:
        return file_reference.target

    # Uses the file_reference_dirs to fetch the root path.
    root_dir = file_reference_dirs[file_reference.file_source.value]
    full_path = f"{root_dir}/{file_reference.target}"
    return full_path
