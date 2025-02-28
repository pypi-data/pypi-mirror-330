"""Access information about the connected driver inputs.

This module is only applicable to the Conductor::job
node, not the Conductor::submitter node, whose inputs are
jobs.

Attributes:
    DRIVER_TYPES (dict): A mapping of information about inputs
    is used in the output_directory expression.
"""
import hou
import os
from ciopath.gpath_list import PathList

from ciohoudini import (
    render_rops,
)


def get_single_dirname(parm):
    path = parm.eval()
    path = os.path.dirname(path)
    if not path:
        return "INVALID FILENAME IN {}".format(parm.path())
    return path


def get_ris_common_dirname(parm):
    node = parm.node()
    num = parm.eval()
    path_list = PathList()
    for i in range(num):
        path = node.parm("ri_display_{}".format(i)).eval()

        if path:
            path_list.add(path)

    common_dirname = path_list.common_path().fslash()
    if num == 1:
        common_dirname = os.path.dirname(common_dirname)

    return common_dirname


def no_op(parm):
    return "UNKNOWN INPUT"



DRIVER_TYPES = {
    "ifd": {
        "dirname_func": get_single_dirname,
        "parm_name": "vm_picture",
        "is_simulation": False,
        "conductor_product": "built-in: Mantra",
    },
    "vray_renderer": {
        "dirname_func": get_single_dirname,
        "parm_name": "SettingsOutput_img_file_path",
        "is_simulation": False,
        "conductor_product": "v-ray-houdini",
    },
    "baketexture::3.0": {
        "dirname_func": get_single_dirname,
        "parm_name": "vm_uvoutputpicture1",
        "is_simulation": False,
        "conductor_product":  "built-in: Bake texture",
    },
    "arnold": {
        "dirname_func": get_single_dirname,
        "parm_name": "ar_picture",
        "is_simulation": False,
        "conductor_product": "arnold-houdini",
    },
    "ris::3.0": {
        #"dirname_func": get_ris_common_dirname,
        "dirname_func": get_single_dirname,
        "parm_name": "ri_displays",
        "is_simulation": False,
        "conductor_product": "renderman-houdini",
    },
    # Todo: We need to support the Renderman denoise
    # However we need to find a valid value for the parm_name
    # as there is none at this time
    # "denoise::3.0": {
    #    #"dirname_func": get_ris_common_dirname,
    #    "dirname_func": get_single_dirname,
    #    "parm_name": "output",
    #    "is_simulation": False,
    #    "conductor_product": "renderman-houdini",
    #},
    "Redshift_ROP": {
        "dirname_func": get_single_dirname,
        #"parm_name": "vm_picture",
        "parm_name": "RS_outputFileNamePrefix",
        "is_simulation": False,
        "conductor_product": "redshift-houdini",
    },
    "karma": {
        "dirname_func": get_single_dirname,
        "parm_name": "picture",
        "is_simulation": False,
        #"conductor_product": "karma-houdini",
        "conductor_product": "built-in: karma-houdini",
    },
    "usdrender": {
        "dirname_func": get_single_dirname,
        "parm_name": "outputimage",
        #"parm_name": "lopoutput",
        "is_simulation": False,
        #"conductor_product": "built-in: usdrender-houdini",
        "conductor_product": "built-in: karma-houdini",
    },
    "usdrender_rop": {
        "dirname_func": get_single_dirname,
        "parm_name": "outputimage",
        "is_simulation": False,
        "conductor_product": "built-in: usdrender_rop_houdini",
    },

    "geometry": {
        "dirname_func": get_single_dirname,
        "parm_name": "sopoutput",
        "is_simulation": False,
        "conductor_product":  "built-in: Geometry cache",
    },
    "output": {
        "dirname_func": get_single_dirname,
        "parm_name": "dopoutput",
        "is_simulation": True,
        "conductor_product":  "built-in: Simulation",
    },
    "dop": {
        "dirname_func": get_single_dirname,
        "parm_name": "dopoutput",
        "is_simulation": True,
        "conductor_product": "built-in: Simulation",
    },
    "opengl": {
        "dirname_func": get_single_dirname,
        "parm_name": "picture",
        "is_simulation": False,
        "conductor_product": "built-in: OpenGL render",
    },
    "unknown": {
        "dirname_func": no_op,
        "parm_name": None,
        "is_simulation": False,
        "conductor_product":  "unknown driver",
    },
}
def set_usdrender_node_renderer(node):
    """Set the renderer type on the usdrender node."""


def apply_image_output_script(rop_path, script):
    """Apply the given script to the given rop."""
    if rop_path:
        rop_node = hou.node(rop_path)
        if rop_node:
            # print("rop: {}".format(rop_node.name()))
            driver_type = rop_node.type().name()
            callback = DRIVER_TYPES.get(driver_type, DRIVER_TYPES["unknown"])

            parm = rop_node.parm(callback["parm_name"])
            if parm:
                # If parm value is empty
                # then set it to the script.
                if not parm.eval():
                    # print("Setting parm: {} with script {}".format(parm.name(), script))
                    parm.set(script)
                else:
                    print("Skipping parm: {} with script {}, parm is not empty".format(parm.name(), script))
            else:
                print("Error: Could not find parm: {}".format(callback["parm_name"]))
        else:
            print("Error: Could not find rop: {}".format(rop_path))
def is_simulation(input_type):
    """Is the source node to be treated as a simulation?

    This means the frame range will not be split into chunks
    and no frame spec UI will be shown.
    """
    dt = DRIVER_TYPES.get(input_type, DRIVER_TYPES["unknown"])
    return dt["is_simulation"]

def get_driver_data(node):
    """Get the whole driver data associated with the connected input."""
    driver_node = hou.node(node.parm('driver_path').evalAsString())
    if not driver_node:
        return DRIVER_TYPES["unknown"]
    driver_type = driver_node.type().name()
    return DRIVER_TYPES.get(driver_type, DRIVER_TYPES["unknown"])

def get_driver_node(node):
    """Get connected driver node or None."""
    return hou.node(node.parm("driver_path").evalAsString())

def update_input_node(node):
    """Callback triggered every time an input connection is made/broken.

    We update UI in 2 ways:

    1. Show the type and the path to the input node.
    2. Remove the frame range override section if the node is a simulation. While it may be possible
       that a user wants to sim an irregular set of frames, it is very unlikely and clutters the UI.


    """
    input_nodes = node.inputs()
    connected = input_nodes and input_nodes[0]
    path = input_nodes[0].path() if connected else ""
    node.parm("driver_path").set(path)
    if connected:
        render_rops.add_render_ropes(node)


def calculate_output_path(node):

    driver_node = hou.node(node.parm('driver_path').evalAsString())
    if not driver_node:
        return "CONNECT A DRIVER NODE"
    driver_type = driver_node.type().name()
    callback = DRIVER_TYPES.get(driver_type, DRIVER_TYPES["unknown"])

    parm = driver_node.parm(callback["parm_name"])
    return callback["dirname_func"](parm)


