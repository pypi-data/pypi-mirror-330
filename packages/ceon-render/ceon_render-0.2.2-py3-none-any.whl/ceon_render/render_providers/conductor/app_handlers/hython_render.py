#!/usr/bin/env hython
# TODO Modify to support setting render resolution

"""Script to render a ROP.

# Task template should resolve to something like:
# hython "/Users/julian/Conductor/houdini/ciohoudini/scripts/chrender.py" -f 2 2 1 -d /out/mantra1 "/path/to/aaa_MantraOnly.hip"
"""

import subprocess
import sys
import os
import re
import argparse

from string import ascii_uppercase
import hou

SIM_TYPES = ("baketexture", "geometry", "output", "dop")

DRIVE_LETTER_RX = re.compile(r"^[a-zA-Z]:")


def error(msg):
    if msg:
        sys.stderr.write("\n")
        sys.stderr.write("Error: %s\n" % msg)
        sys.stderr.write("\n")
        sys.exit(1)


def usage(msg=""):
    sys.stderr.write(
        """Usage:

    hython /path/to/chrender.py -d driver -f start end step hipfile
    All flags/args are required

    -d driver:          Path to the output driver that will be rendered
    -f range:           The frame range specification (see below)
    -r resolution:      The pixel dimensions of the rendered frame, width height
    hipfile             The hipfile containing the driver to render
    """
    )
    error(msg)


def set_hip_env(env_name, env_value):
    hou.putenv(env_name, env_value)
    print(f"Set {env_name} to: {hou.getenv(env_name)}")

    # Trigger scene to recook/recognize changes.
    # hou.hscript('varchange')

    # Allow the variable to OVERWRITE the variables if it was already set in the hipfile.
    os.environ[env_name] = env_value
    hou.allowEnvironmentToOverwriteVariable(env_name, True)


def prep_ifd(node):
    """Prepare the IFD (Mantra) ROP for rendering."""
    print("Preparing Mantra ROP node {}".format(node.name()))
    node.parm("vm_verbose").set(3)
    print("Set loglevel to 3")
    node.parm("vm_alfprogress").set(True)
    print("Turn on Alfred style progress")
    node.parm("soho_mkpath").set(True)
    print("Make intermediate directories if needed")


def prep_baketexture(node):
    """Prepare the BAKETEXTURE ROP for rendering."""
    pass


def prep_arnold(node):
    """Prepare the Arnold ROP for rendering."""

    print("Preparing Arnold ROP node {} ...".format(node.name()))

    try:
        if node is not None:
            print("Abort on license failure")
            node.parm("ar_abort_on_license_fail").set(True)
            print("Abort on error")
            node.parm("ar_abort_on_error").set(True)
            print("Log verbosity to debug")
            node.parm("ar_log_verbosity").set("debug")
            print("Enable log to console")
            node.parm("ar_log_console_enable").set(True)

            # Setting environment variable ARNOLD_ADP_DISABLE to True
            # Todo: This should have been implemented as a sidecar. Remove this once confirmed and tested.
            # print("Setting environment variable ARNOLD_ADP_DISABLE to True.")
            # os.environ['ARNOLD_ADP_DISABLE'] = '1'

            # Todo: should we allow this?
            # print("Setting environment variable ARNOLD_CER_ENABLED to False.")
            # os.environ['ARNOLD_CER_ENABLED'] = '0'

    except Exception as e:
        print("Error preparing Arnold ROP: {}".format(e))


def prep_redshift(node):
    """Prepare the redshift ROP for rendering."""
    print("Preparing Redshift ROP node {}".format(node.name()))

    print("Turning on abort on license fail")
    node.parm("AbortOnLicenseFail").set(True)

    print("Turning on abort on altus license fail")
    node.parm("AbortOnAltusLicenseFail").set(True)

    print("Turning on abort on Houdini cooking error")
    node.parm("AbortOnHoudiniCookingError").set(True)

    print("Turning on abort on missing resource")
    node.parm("AbortOnMissingResource").set(True)

    print("Turning on Redshift log")
    node.parm("RS_iprMuteLog").set(False)


def prep_karma(node):
    """Prepare the karma ROP for rendering."""
    print("Preparing Karma ROP node {}".format(node.name()))

    # Set the frame output resolution
    resolution = ARGS.resolution
    if resolution:
        print(f"Setting render resolution: {resolution}")
        node.parm("resolutionx").set(resolution[0])
        node.parm("resolutiony").set(resolution[1])

    out_file = ARGS.out_file
    if out_file:
        print(f"Setting out_file: {out_file}")
        node.parm("picture").set(out_file)

    print("Turning on Abort for missing texture")
    node.parm("abortmissingtexture").set(True)

    print("Turning on make path")
    node.parm("mkpath").set(True)

    # print("Turning on save to directory")
    # node.parm("savetodirectory").set(True)

    # print("Turning on Husk stdout")
    # node.parm("husk_stdout").set(True)

    # print("Turning on Husk stderr")
    # node.parm("husk_stderr").set(True)

    print("Turning on Husk debug")
    node.parm("husk_debug").set(True)

    print("Turning on log")
    node.parm("log").set(True)

    print("Turning on verbosity")
    node.parm("verbosity").set(True)

    print("Turning on Alfred style progress")
    node.parm("alfprogress").set(True)

    # Todo: should we allow this?
    # print("Turning on threads")
    # node.parm("threads").set(True)


def prep_usdrender(node):
    """Prepare the usdrender OUT for rendering."""
    print("Preparing usdrender OUT node {}".format(node.name()))
    # Set the frame output resolution
    resolution = ARGS.resolution
    if resolution:
        print(f"Setting usdrender override_res: 'specific'")
        node.parm("override_res").set("specific")
        print(f"Setting render resolution: {resolution}")
        node.parm("res_user").set(
            (
                resolution[0],
                resolution[1],
            )
        )
        # node.parm("resolutiony").set(resolution[1])

    out_file = ARGS.out_file
    if out_file:
        print(f"Setting out_file: {out_file}")
        node.parm("outputimage").set(out_file)

    print("Turning on Alfred style progress")
    node.parm("alfprogress").set(True)

    print("Turning on Husk debug")
    node.parm("husk_debug").set(True)

    # print("Turning on verbosity")
    # node.parm("verbosity").set(True)

    print("Turning on husk_log")
    node.parm("husk_log").set(True)

    # print("Turning on Husk stdout")
    # node.parm("husk_stdout").set(True)

    # print("Turning on Husk stderr")
    # node.parm("husk_stderr").set(True)

    # print("Turning on Save Time Info")
    # node.parm("savetimeinfo").set(True)

    print("Turning on Make Path")
    node.parm("mkpath").set(True)


# TODO is this the out context? The above is the LOPS context?
def prep_usdrender_rop(node):
    """Prepare the usdrender OUT for rendering."""
    print("Preparing usdrender rop node {}".format(node.name()))

    out_file = ARGS.out_file
    if out_file:
        print(f"Setting out_file: {out_file}")
        node.parm("outputimage").set(out_file)
    else:
        print("WARNING: Did not receive out_file args. Using default from hipfile")

    # Set the frame output resolution
    resolution = ARGS.resolution
    if resolution:
        print(f"Setting usdrender override_res: 'specific'")
        node.parm("override_res").set("specific")
        print(f"Setting render resolution: {resolution}")
        node.parmTuple("res_user").set(
            (
                resolution[0],
                resolution[1],
            )
        )
        # node.parm("resolutiony").set(resolution[1])

    print("Turning on Alfred style progress")
    node.parm("alfprogress").set(True)

    print("Turning on Husk debug")
    node.parm("husk_debug").set(True)

    print("Turning on husk_log")
    node.parm("husk_log").set(True)

    print("Turning on Make Path")
    node.parm("mkpath").set(True)


def prep_ris(node):
    """
    Prepares the Renderman ROP (RIS) for rendering by setting specific parameters.

    This function configures the Renderman ROP by adjusting its log level and enabling progress reporting. Additionally, it ensures that intermediate directories are created for each display defined in the ROP. This preparation is crucial for rendering tasks, ensuring that log verbosity is sufficient for debugging and that necessary directories are available for output files.

    Parameters:
    node (hou.Node): The Renderman ROP node to prepare.
    """
    print("Preparing Ris ROP node {}".format(node.name()))
    node.parm("loglevel").set(4)
    print("Set loglevel to 4")
    node.parm("progress").set(True)
    print("Turn progress on")
    num_displays = node.parm("ri_displays").eval()
    for i in range(num_displays):
        print("Set display {} to make intermediate directories if needed".format(i))
        node.parm("ri_makedir_{}".format(i)).set(True)


def prep_vray_renderer(node):
    """
    Prepares the V-Ray ROP for rendering.

    Currently, this function does not perform any preparation due to the lack of specific V-Ray parameters that need adjusting in this context. This placeholder indicates where V-Ray specific preparation steps would be implemented if needed.

    Parameters:
    node (hou.Node): The V-Ray ROP node to prepare.
    """

    print("Preparing V-Ray ROP node {}".format(node.name()))
    # I couldn't find a parameter to increase verbosity or set progress format.
    print("Nothing to do")


def prep_geometry(node):
    """
    Prepares the geometry ROP for rendering.

    This function is currently a placeholder and does not implement any preparation steps. It's intended to be a template for future implementations where specific preparation of the geometry ROP might be required.

    Parameters:
    node (hou.Node): The geometry ROP node to prepare.
    """
    pass


def prep_output(rop_node):
    """
    Prepares the output ROP for rendering.

    This function is currently a placeholder and does not implement any preparation steps. It serves as a template for future implementations where specific preparation of the output ROP might be necessary.

    Parameters:
    rop_node (hou.Node): The output ROP node to prepare.
    """
    pass


def prep_dop(node):
    """
    Prepares the DOP ROP for rendering by setting specific parameters.

    This function adjusts the DOP ROP to enable the creation of necessary directories, to render over a time range, and to report progress. These adjustments are crucial for dynamic simulations where output management and progress tracking are essential.

    Parameters:
    node (hou.Node): The DOP ROP node to prepare.
    """
    node.parm("trange").set(1)
    node.parm("mkpath").set(True)
    node.parm("alfprogress").set(True)


def prep_opengl(node):
    """
    Prepares the OpenGL ROP for rendering.

    This function is currently a placeholder and does not implement any preparation steps. It's intended to be a template for future implementations where specific preparation of the OpenGL ROP might be required.

    Parameters:
    node (hou.Node): The OpenGL ROP node to prepare.
    """
    pass


def run_driver_prep(rop_node):
    """
    Executes the appropriate preparation function for a given ROP based on its type.

    This function dynamically identifies and runs a preparation function specific to the type of the provided ROP node. It's designed to automate the setup process for different ROP types, enhancing rendering workflows. If no specific preparation function exists for the ROP type, the function silently completes without action.

    Parameters:
    rop_node (hou.Node): The ROP node for which to run preparation.
    resolution: Optional frame dimensions (width, height) to overwrite output resolution. Only applies to render nodes.
    """

    rop_type = rop_node.type().name().split(":")[0]
    try:
        fn = globals()["prep_{}".format(rop_type)]
        print("Running prep function for ROP type: {}".format(rop_type))
        print("Function: {}".format(fn))
    except KeyError:
        return
    try:
        fn(rop_node)

    except Exception as e:
        sys.stderr.write(
            "Failed to run prep function for ROP type: {}. Skipping.\n".format(rop_type)
        )
        sys.stderr.write(f"{e}")
        return


def is_sim(rop):
    """
    Determines if the given ROP is of a simulation type.

    This function checks the type of the provided ROP node against a predefined list of simulation types. It returns True if the ROP is identified as a simulation type, indicating that it may require specific handling during rendering processes.

    Parameters:
    rop (hou.Node): The ROP node to check.

    Returns:
    bool: True if the ROP is a simulation type, False otherwise.
    """
    return rop.type().name().startswith(SIM_TYPES)


def parse_args():
    """
    Parses command-line arguments for the script, ensuring required arguments are provided.

    This function sets up argument parsing for the script, specifying that the driver and hipfile are required arguments, while frames is an optional argument that expects three integer values. It uses the argparse library to define these requirements and handle parsing.

    Arguments:
    -d (str): The driver argument, required for operation.
    -f (int int int): A series of three integers representing the frame range, optional.
    hipfile (str): The path to the hip file, required.

    If any unknown arguments are provided, the script prints an error message indicating the unrecognized arguments and halts execution. This ensures that only the expected arguments are passed to the script.

    Returns:
    argparse.Namespace: An object containing the parsed arguments. This object will have attributes for 'driver', 'frames' (if provided), 'resolution' (if provided) and 'hipfile'.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("hipfile", nargs=1, type=str)
    parser.add_argument("driver", type=str)
    parser.add_argument("-f", dest="frames", nargs=3, type=int)
    parser.add_argument("-r", dest="resolution", nargs=2, type=int, required=False)
    parser.add_argument(
        "-o",
        "-out-file",
        dest="out_file",
        type=str,
        required=False,
        help="Replace the rop output full filepath. E.g. $HIP/render/thisNameFromScript.$F4.exr",
    )
    parser.add_argument(
        "-scene-vars",
        "-vars",
        dest="scene_vars",
        type=str,
        nargs="+",
        help="Houdini variables to set. Overwrites existing hip vars if they already exist. Syntax is VARNAME=VALUE",
    )

    args, unknown = parser.parse_known_args()

    if unknown:
        usage("Unknown argument(s): %s" % (" ".join(unknown)))

    return args


def ensure_posix_paths():
    """
    Converts file paths in Houdini file references to POSIX format.

    This function iterates over all file references in the current Houdini session. For each reference, it checks if the path contains a Windows-style drive letter. If so, it strips the drive letter and converts backslashes to forward slashes, thereby converting the path to POSIX format. This conversion is essential for ensuring compatibility across different operating systems, particularly when moving projects from Windows to Unix-like systems.

    The function skips over references that do not contain a Windows-style drive letter or are part of nodes with a type that starts with "conductor::job", assuming these references do not require conversion. For each conversion, it prints both the original path and the converted path for verification purposes. If setting the new path fails, it catches the exception, prints an error message, and continues with the next file reference.
    """

    refs = hou.fileReferences()

    for parm, value in refs:
        if not parm:
            continue

        try:
            node_name = parm.node().name()
            parm_name = parm.name()
            node_type = parm.node().type().name()
        except:
            print("Failed to get parm info")
            continue
        ident = "[{}]{}.{}".format(node_type, node_name, parm_name)
        if node_type.startswith("conductor::job"):
            continue

        if not DRIVE_LETTER_RX.match(value):
            print("Not a drive letter. Skipping")
            continue

        print("{} Found a drive letter in path: {}. Stripping".format(ident, value))
        value = DRIVE_LETTER_RX.sub("", value).replace("\\", "/")
        print("{} Setting value to {}".format(ident, value))
        try:
            parm.set(value)
        except hou.OperationFailed as ex:
            print("{} Failed to set value for parm {}. Skipping".format(ident, value))
            print(ex)
            continue
        print("{} Successfully set value {}".format(ident, value))


def render(args):
    """
    Render the specified Render Operator (ROP) within a Houdini scene based on the arguments provided.

    This function takes command line arguments to specify the Houdini project file (.hip file),
    the driver node (ROP) to render, and the frame range for rendering. It attempts to load the
    specified .hip file and, if successful, proceeds to render the specified ROP. If the .hip file
    loads with only warnings, it prints these warnings and continues with the rendering process.
    If the specified ROP does not exist, it lists the available ROPs in the scene.

    Parameters:
        args: A namespace object containing the following attributes:
            - hipfile (str): The path to the .hip file to be loaded.
            - driver (str): The path to the ROP node that will be rendered.
            - frames (tuple): A tuple specifying the start frame, end frame, and frame step.
            - resolution (tuple): A tuple specifying the width and height of the rendered frames.

    Note:
        If the .hip file contains unknown assets or nodes that only produce warnings upon loading,
        these warnings are printed out.

    Raises:
        hou.LoadWarning: If there are any issues loading the .hip file, a warning is printed,

    """

    # Unpack the arguments
    hipfile = args.hipfile[0]
    driver = args.driver
    frames = args.frames
    resolution = args.resolution
    scene_vars = args.scene_vars
    out_file = args.out_file

    # Print out the arguments
    print("hipfile: '{}'".format(hipfile))
    print("driver: '{}'".format(driver))
    print("frames: 'From: {} to: {}'by: {}".format(*frames))
    print(f"resolution: {resolution}")
    print(f"out_file: {out_file}")

    print("\n--Preparing vars...")
    # Set hip variables BEFORE loading the scene so that they are
    # recognized by node/hda onLoad events.
    test_scene_vars = [
        "ENV_VIA_API=SUCCESS via new script",
        "ENV_TO_OVERWRITE=SUCCESS overwritten via new script",
    ]
    if not scene_vars:
        scene_vars = test_scene_vars
    # for var in scene_vars:
    for var in scene_vars:
        varname, value = var.split("=")
        set_hip_env(varname, value)

    print("\n--Loading hipfile...")
    # Load the hip file
    try:
        hou.hipFile.load(hipfile)
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e)

    rop = hou.node(driver)
    if rop:
        render_rop(rop, frames)
    # If the specified ROP does not exist, print the available ROPs in the scene.
    else:
        msg = "ROP does not exist: '{}' \n".format(driver)
        sys.stderr.write(msg)
        print_available_rops()
        return


def print_available_rops():
    """
    Prints the list of available Render Operators (ROPs) in the current Houdini session to stderr.

    This function attempts to retrieve and list all ROP nodes available within the scene. If any
    error occurs during the retrieval process, it prints an error message indicating the failure
    to list the available ROPs.

    Note:
        This function is typically called when a specified ROP does not exist or cannot be found,
        to assist the user in identifying the correct ROP to use.

    Raises:
        Exception: If an error occurs while attempting to retrieve the list of available ROPs,
                    an error message is printed to stderr.
    """
    try:
        # Print out the available ROPs
        all_rops = hou.nodeType(hou.sopNodeTypeCategory(), "ropnet").instances()
        sys.stderr.write("Available ROPs:\n")
        for r in all_rops:
            sys.stderr.write("  {}\n".format(r.path()))
        return
    except Exception as e:
        sys.stderr.write("Failed to get available ROPs\n")


def render_rop(
    rop: hou.Node,
    frames: tuple[int],
):
    """
    Executes the rendering process for a specified Render Operator (ROP) based on a provided frame range.

    This function is responsible for rendering a specific ROP node within a Houdini scene. It ensures that all
    file paths are POSIX-compliant, runs any driver-specific preparation tasks, and then initiates the rendering
    process. The function handles different types of ROPs as follows:

    - If the ROP node is of type 'topnet', it uses the cook() method to process the TOP network.
    - If the ROP node is a simulation type, identified by the is_sim() function, it uses the render() method
      without a frame range.
    - For all other ROP types, it uses the render() method with the specified frame range.

    Parameters:
        rop (hou.Node): The ROP node to be rendered.
        frames (tuple): A tuple specifying the start frame, end frame, and frame step for the render.
        resolution (tuple): A tuple specifying the width and height of the rendered frame. If None, uses the existing resolution set on the node

    Note:
        This function assumes that all necessary preparations for rendering (such as path normalization
        and driver-specific preparations) are completed within it.

    Raises:
        hou.OperationFailed: If the rendering process encounters an error, an exception is caught and
                             an error message is printed to stderr. The function then exits without
                             completing the render process.

    Example:
        render_rop(rop_node, (1, 100, 1))
        This would render the specified ROP node from frame 1 to frame 100 with a step of 1.
    """
    try:
        print("Ensure POSIX paths")
        ensure_posix_paths()
        run_driver_prep(rop)
        # Prepare the ROP for rendering based on its type
        # If the ROP is a TOP network, use cookWorkItems() instead of render
        if rop.type().name() == "topnet":
            rop.displayNode().cookWorkItems(block=True)
        # If the ROP is a simulation type, render without a frame range
        elif is_sim(rop):
            rop.render(verbose=True, output_progress=True)
        # Otherwise, render with the specified frame range
        else:
            rop.render(
                frame_range=tuple(frames),
                verbose=True,
                output_progress=True,
                method=hou.renderMethod.FrameByFrame,
            )
    except hou.OperationFailed as e:
        sys.stderr.write("Error rendering the rop: %s\n" % e)
        return


ARGS = parse_args()
render(ARGS)
