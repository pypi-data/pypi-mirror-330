import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ConductorPayload:
    """
    Stores all of the required arguments to build a payload for submission
    via Conductor's API
    App Agnostic (use specific app functions to build this payload according
    to a particular app's requirements)

    instance_type:
        Can be fetched with ciocore.app_client.request_instance_types
        cpu syntax:
            {provider}-xeonv3-{num_cores}
            cw-xeonv3-64
                cw = cloudweave (provider)
                64 cores
    """

    job_title: str
    project: str
    tasks_data: list[dict]
    output_path: str
    # instance_type: str = "cw-xeonv3-8"
    instance_type: str = "cw-xeonv3-32"
    preemptible: bool = True
    autoretry_policy: dict = field(
        default_factory=lambda: {"preempted": {"max_retries": 3}}
    )
    # TODO workflow that doesn't assume app/packages?
    software_package_ids: list = field(
        default_factory=lambda: ["29f7765dc99e417596d5145afc012338"]
    )  # Hou 20.0.547
    # TODO get environment dynamically
    print("TODO: Get submission environment dynamically")
    environment: dict = field(
        default_factory=lambda: {
            "HFS": "/opt/sidefx/houdini/20/houdini-20.5.410",
            "HOUDINI_HSERVER_USE_HTTP": "0",
            "HB": "/opt/sidefx/houdini/20/houdini-20.5.410/bin",
            "PATH": "/opt/sidefx/houdini/20/houdini-20.5.410/bin:/opt/sidefx/houdini/20/houdini-20.5.410/houdini/sbin",
            "HOUDINI_PATH": "&",
            "HOUDINI_PATHMAP": "{'a:/': '/', 'b:/': '/', 'c:/': '/', 'd:/': '/', 'e:/': '/', 'f:/': '/', 'g:/': '/', 'h:/': '/', 'i:/': '/', 'j:/': '/', 'k:/': '/', 'l:/': '/', 'm:/': '/', 'n:/': '/', 'o:/': '/', 'p:/': '/', 'q:/': '/', 'r:/': '/', 's:/': '/', 't:/': '/', 'u:/': '/', 'v:/': '/', 'w:/': '/', 'x:/': '/', 'y:/': '/', 'z:/': '/'}",
            "SESI_LMHOST": "conductor-hlm:1715",
            "CONDUCTOR_PATHHELPER": "0",
            # "JOB": "/mnt/FileStorage/Dayne/Web/proj_ceonstock/tests/cloud_rendering/conductor/hou_project_basic",
            "OCIO": "/home/dayne/Apps/sidefx/hfs20.0.547/packages/ocio/houdini-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio",
        }
    )
    local_upload: bool = True
    scout_frames: str = ""
    upload_paths: list[str] = field(default_factory=list)

    def as_dict(self):
        return asdict(self)


class ConductorTaskData:
    """Build the task_data to be passed to the Conductor payload
    Currently assumes houdini/hython
    """

    def __init__(
        self,
        script_path: str,
        scenefile: str,
        driver: str,  # The houdini node to render
        frames: tuple[int, int, int],  # Start, stop, step
        resolution: tuple[int, int],  # Width, height
        vars: list[str],  # Overwrite envs in hipfile
        out_file: str,  # Set the houdini output ROP to this value.
    ):
        """
        vars: A list of ["ENV_TO_SET=Value"] strings to overwrite existing vars in the hipfile.
        """
        self.script_path = script_path
        self.scenefile = scenefile
        self.driver = driver
        self.frames = frames
        self.resolution = resolution
        self.vars = vars
        self.out_file = out_file

    def cmds_list(self) -> list[str]:
        """Return cmds as a list of strings to be executed by the cmdline"""
        # Use single quotes instead of double quotes to prevent string expansion in console.
        # This is required for $F4 values in houdini filenames
        cmd = [
            "hython",
            f"'{self.script_path}'",
            f"'{self.scenefile}'",
            f"'{self.driver}'",
            "-f",
            self.frames[0],
            self.frames[1],
            self.frames[2],
            "-r",
            self.resolution[0],
            self.resolution[1],
        ]
        if self.out_file:
            cmd += ["-o", f"'{self.out_file}'"]
        if self.vars:
            vars_to_set = [f"'{var}'" for var in self.vars]
            cmd += ["-vars", *vars_to_set]
        cmds_stringified = [str(cmd) for cmd in cmd]
        return cmds_stringified

    def cmds_string(self):
        return " ".join(self.cmds_list())

    def as_dict(self) -> dict[str, Any]:
        """Return a dict containing the task data as expected by the Payload"""
        # Format frames as a single digit if start/end are the same
        frames_str = (
            f"{self.frames[0]}-{self.frames[1]}"
            if self.frames[1] - self.frames[0] != 0
            else self.frames[0]
        )
        task_data = {"command": self.cmds_string(), "frames": str(frames_str)}
        return task_data


def prepare_frame_batches(
    frames: tuple[int, int, int], batch_size
) -> list[tuple[int, int, int]]:
    """Break a frame range down into a list of multiple batches."""
    # Currently assumes batch_size = 1
    num_frames = frames[1] - frames[0] + 1
    num_batches = math.ceil(num_frames / batch_size)
    frame_batches = []
    for batch_num in range(num_batches):
        batch_offset = batch_num * batch_size
        start_frame = frames[0] + batch_offset
        end_frame = frames[0] + batch_offset + batch_size - 1
        # Handle case where final batch contains less frames than other batches
        end_frame = min(end_frame, frames[1])
        # Currently assumes step=1
        batch_frames = (start_frame, end_frame, 1)
        frame_batches.append(batch_frames)
    return frame_batches


def prepare_task_datas(
    *,
    script_file: str,
    scene_file: str,
    output_file: str,
    driver: str,
    frames: tuple[int, int, int],
    resolution: tuple[int, int],
    batch_size: int,
    vars: list[str] | None = None,
) -> list[ConductorTaskData]:
    """
    vars: A list of strings to set env vars: ["VAR_TO_SET=VALUE", ...]
    """
    if not vars:
        vars = []
    # Prevent $s from being escaped in terminal so they can be correctly passed to houdini
    # output_file = output_file.replace("$", r"\$")
    frame_batches = prepare_frame_batches(frames, batch_size)
    task_datas = []
    for frame_batch in frame_batches:
        task_data = ConductorTaskData(
            script_path=script_file,
            scenefile=scene_file,
            driver=driver,
            frames=frame_batch,
            out_file=output_file,
            resolution=resolution,
            vars=vars,
        )
        task_datas.append(task_data)
    return task_datas


def create_payload(
    job_title: str,
    project: str,
    script_filepath: str,
    scene_filepath: str,
    output_path: str,
    driver: str,  # The houdini node to render
    frames: tuple[int, int, int],
    resolution: tuple[int, int],
    vars: dict[str, str],  # Overwrite envs in hipfile
    batch_size: int = 2,
    upload_paths: list | None = None,
) -> ConductorPayload:
    if not upload_paths:
        upload_paths = []
    # TODO batching frames.
    vars_formatted = [f"{key}={value}" for key, value in vars.items()]
    task_datas = prepare_task_datas(
        script_file=script_filepath,
        scene_file=scene_filepath,
        driver=driver,
        frames=frames,
        resolution=resolution,
        output_file=output_path,
        batch_size=batch_size,
        vars=vars_formatted,
    )
    task_datas_serialized = [task_data.as_dict() for task_data in task_datas]
    output_dir = str(Path(output_path).parent)
    payload = ConductorPayload(
        job_title=job_title,
        project=project,
        tasks_data=task_datas_serialized,
        output_path=output_dir,
        upload_paths=upload_paths,
    )
    return payload
