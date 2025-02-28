"""frame range section in the UI."""

import hou

def resolve_payload(node, rop_path):
    title = node.parm("title").eval().strip()
    title = "{}  {}".format(title, rop_path)
    return {"job_title": title}

