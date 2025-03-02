from pathlib import Path
import json
import uuid

from ciocore import conductor_submit

import ceonstock_render_conductor as crc

OUT_DIR = str(Path("./conductor_outputs").resolve().absolute())
# OUT_DIR = str(
#     Path(
#         f"/mnt/FileStorage/Dayne/Web/proj_ceonstock/tests/cloud_rendering/conductor/hou_project_basic/render"
#     )
#     .resolve()
#     .absolute()
# )
PROJECT_DIR = str(Path("./hou_project_basic").resolve().absolute())
HIPFILE_NAME = "simple_box.hiplc"
HIPFILE = str(Path(PROJECT_DIR, HIPFILE_NAME).resolve().absolute())
SCRIPT_FILE = str(
    Path("./ceonstock_render_conductor/chrender_ceonstock.py")
    .resolve()
    .absolute()
)


# def submit_payload(payload: crc.ConductorPayload):
#     data = payload.as_dict()
#     submission = conductor_submit.Submit(data)
#     response, response_code = submission.main()
#     print(response_code)
#     print(json.dumps(response))


def main():
    upload_paths = [
        str(PROJECT_DIR),
        str(SCRIPT_FILE),
        str(HIPFILE),
    ]
    # The output_path needs to also be the path that the files are actually written to, otherwise
    # they can't be detected for download.
    # Files that are sub-paths of output_path will also be downloaded.
    random_uuid = uuid.uuid4().hex[:8]
    output_filename = f"{random_uuid}/namedFromScript.$F4.exr"
    output_path = str(Path(OUT_DIR, output_filename))
    payload = crc.conductor_payload.create_payload(
        job_title="move driver to positional arg",
        project="api_testing",
        script_filepath=SCRIPT_FILE,
        scene_filepath=HIPFILE,
        driver="/out/karma_cpu",
        frames=(1, 4, 1),
        resolution=(960, 540),
        vars=[],
        upload_paths=upload_paths,
        output_path=output_path,
        batch_size=2,
    )
    print("Created payload")
    payload_dict = payload.as_dict()
    print(json.dumps(payload_dict, indent=2))
    crc.submit.submit_payload(payload)


if __name__ == "__main__":
    main()
