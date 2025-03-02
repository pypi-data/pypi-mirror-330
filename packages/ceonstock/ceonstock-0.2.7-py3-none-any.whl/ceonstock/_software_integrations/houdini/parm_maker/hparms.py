# Provides functionality for interacting with houdini parms.
# This module is ceonstock AGNOSTIC.
import hou
from typing import List
from typing import Optional, Tuple


def get_visible_parms(parms):
    """
    Assumes all provides parms belong to the same node
    Checks if the parm is currently visible in the UI
    Returns only parms that are visible
    """
    parms[0].node().updateParmStates()
    visible_parms = [parm for parm in parms if not is_parm_hidden(parm)]
    return visible_parms


def create_parm(parm_data: dict, debug=False):
    # Takes a dictionary defining the parm to be created.
    # Example data:
    # {
    # "type": hou.FolderParmTemplate,
    # "name": "my_folder",
    # "label": "New Folder",
    # "folder_type": hou.folderType.Tabs,
    # "_children": [] # List of objects with same format as above
    # }
    if debug:
        print(f"{parm_data}\ncreate_parm got parm_data: ")
    parm_data = parm_data.copy()
    parm_type = parm_data.pop("type")
    if parm_type == hou.FolderParmTemplate:
        try:
            parm_data_list = parm_data.pop("_children")
        except KeyError:
            parm_data_list = []
        folder_parm = parm_type(**parm_data)
        for parm_data in parm_data_list:
            if debug:
                print("Creating child_parm from data: ", parm_data)
            child_parm = create_parm(parm_data)
            folder_parm.addParmTemplate(child_parm)
        return folder_parm
    else:
        return parm_type(**parm_data)


def print_templates_in_folder(node, folder_labels: tuple):
    ptg = node.parmTemplateGroup()
    # group_or_folder = ptg.findFolder(("Import", "Imported Data"))
    group_or_folder = ptg.findFolder(folder_labels)
    result = parm_templates_in_folder(group_or_folder)
    print("Found parms in folder {}: ".format(group_or_folder.name()))
    for parm in result:
        print("\t{}".format(parm.name()))
    return result


# Try not to use this. Only if necessary
def recook_scene():
    for node in hou.node("/").allSubChildren():
        node.cook(force=True)


def parm_templates_in_folder(
    group_or_folder, include_parms_in_inner_folders=False
):
    """Takes a parmTemplateGroup/folder as input and returns all input parms (including
    nested inside of other folders), excluding instances inside multiparm blocks.
    """
    to_return = []
    for parm_template in group_or_folder.parmTemplates():
        # Note that we don't want to return parm templates inside multiparm
        # blocks, so we verify that the folder parm template is actually
        # for a folder.
        to_return.append(parm_template)
        name = parm_template.name()
        print("got parm_template: {}".format(name))
        if (
            include_parms_in_inner_folders
            and parm_template.type() == hou.parmTemplateType.Folder
            and parm_template.isActualFolder()
        ):
            print(f"{name} type is folder AND isActualFolder!")
            for sub_parm_template in parm_templates_in_folder(parm_template):
                to_return.append(sub_parm_template)
                print(
                    f"Got sub_parm_template from {name}: {sub_parm_template.name()}"
                )
    return to_return


def parm_tuples_in_folder(
    node: hou.Node,
    folder_parm_template: hou.FolderParmTemplate,
    include_nested=False,
):
    # parm_templates_in_folder = folder_parm_template.parmTemplates()
    parm_templates = parm_templates_in_folder(
        folder_parm_template, include_parms_in_inner_folders=include_nested
    )
    parm_tuples_in_folder = [
        node.parmTuple(parm_template.name())
        for parm_template in parm_templates
    ]
    return parm_tuples_in_folder


def get_multiparm_parms(multiparm: hou.Parm, include_nested=False):
    parm_list = multiparm.multiParmInstances()
    if include_nested:
        for parm in parm_list:
            if is_multiparm(parm):
                parm_list += get_multiparm_parms(parm, include_nested=True)
    return parm_list


def get_multiparm_parms_grouped_by_instance(
    multiparm: hou.Parm, flatten_nested_multiparms: bool = False
):
    """If flatten_nested_multiparms is true, the children of any inner multiparms
    will be included. If false, the children are not included"""
    instance_parms = get_multiparm_parms(
        multiparm, include_nested=flatten_nested_multiparms
    )
    nest_depth = len(multiparm.multiParmInstanceIndices())
    # Group parms by instance
    instance_parms_grouped_by_index = {}
    for instance_parm in instance_parms:
        instance_num = instance_parm.multiParmInstanceIndices()[nest_depth]
        if str(instance_num) not in instance_parms_grouped_by_index.keys():
            instance_parms_grouped_by_index[str(instance_num)] = []
        instance_parms_grouped_by_index[str(instance_num)].append(
            instance_parm
        )

    return instance_parms_grouped_by_index


def create_color_parm(
    name: str,
    label: str,
    default_value: List[float] = [0.5, 0.25, 0.0],
    as_data: bool = False,
    **kwargs,
):
    parm_data = {
        "type": hou.FloatParmTemplate,
        "name": name,
        "label": label,
        "num_components": 3,
        "default_value": default_value,
        "look": hou.parmLook.ColorSquare,
        "naming_scheme": hou.parmNamingScheme.RGBA,
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if as_data:
        return parm_data
    new_parm = create_parm(parm_data)
    return new_parm


def create_toggle_parm(
    name: str,
    label: str,
    default_value: bool = False,
    as_data: bool = False,
    **kwargs,
):
    parm_data = {
        "type": hou.ToggleParmTemplate,
        "name": name,
        "label": label,
        "default_value": default_value,
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}

    if as_data:
        return parm_data
    new_parm = create_parm(parm_data)
    return new_parm


def create_file_parm(
    name: str, label: str, default_value: str = "", as_data=False, **kwargs
):
    if default_value is None:
        default_value = f"$HIP/{label}.jpg"
    parm_data = {
        "type": hou.StringParmTemplate,
        "name": name,
        "label": label,
        "default_value": [default_value],
        "num_components": 1,
        "string_type": hou.stringParmType.FileReference,
        # "file_type": hou.fileType.Image,
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_text_parm(
    name: str,
    label: str,
    default_value: str = "",
    multiline: bool = False,
    as_data: bool = False,
    **kwargs,
):
    parm_data = {
        "type": hou.StringParmTemplate,
        "name": name,
        "label": label,
        "default_value": [default_value],
        "num_components": 1,
        "string_type": hou.stringParmType.Regular,
        # "join_with_next": join_with_next,
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if multiline:
        multiline_tag = {"editor": "1", "editorlines": "5-40"}
        current_tags = parm_data.get("tags", {})
        parm_data["tags"] = {**current_tags, **multiline_tag}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_dropdown_parm(
    name: str,
    label: str,
    dropdown_options: dict,
    default_value: Optional[str] = None,
    as_data: bool = False,
    **kwargs,
):
    # dropdown_options = sorted(dropdown_options)
    menu_values = [
        str(dropdown_option["value"]) for dropdown_option in dropdown_options
    ]
    menu_labels = [
        str(dropdown_option["label"]) for dropdown_option in dropdown_options
    ]
    if default_value is None or default_value not in menu_values:
        default_value = menu_values[0]
    parm_data = {
        "type": hou.StringParmTemplate,
        "name": name,
        "label": label,
        "num_components": 1,
        "default_value": [default_value],
        "menu_items": (menu_values),
        "menu_labels": (menu_labels),
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_int_parm(
    name: str,
    label: str,
    default_value: int = 0,
    as_data: bool = False,
    **kwargs,
):
    parm_data = {
        "type": hou.IntParmTemplate,
        "name": name,
        "label": label,
        "num_components": 1,
        "default_value": [int(default_value)],
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_heading_parm(
    name: str, label: str, text: str, as_data=False, **kwargs
):
    if not text:
        text = ""
    parm_data = {
        "type": hou.LabelParmTemplate,
        "name": name,
        "label": label,
        "column_labels": [text],
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    heading_tag = {"sidefx::look": "heading"}
    current_tags = parm_data.get("tags", {})
    parm_data["tags"] = {**current_tags, **heading_tag}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_message_parm(
    name: str, label: str, text: str, as_data=False, **kwargs
):
    if not text:
        text = ""
    parm_data = {
        "type": hou.LabelParmTemplate,
        "name": name,
        "label": label,
        "column_labels": [text],
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    block_tag = {"sidefx::look": "block"}
    current_tags = parm_data.get("tags", {})
    parm_data["tags"] = {**current_tags, **block_tag}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_label_parm(
    name: str, label: str, text=None, as_data=False, **kwargs
):
    if not text:
        text = ""
    parm_data = {
        "type": hou.LabelParmTemplate,
        "name": name,
        "label": label,
        "column_labels": [text],
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_folder_parm(
    name: str,
    label: str,
    child_parm_data: Optional[list] = None,
    folder_config: Optional[str] = None,
    as_data=False,
    **kwargs,
):
    folder_config_settings = {
        "collapsible": {"folder_type": hou.folderType.Collapsible},
        "borderless": {"tags": {"sidefx::look": "blank"}},
    }
    parm_data = {
        "type": hou.FolderParmTemplate,
        "name": name,
        "label": label,
        "default_value": 1,
    }
    if folder_config:
        # Get the folder config
        try:
            folder_settings = folder_config_settings[folder_config]
        except KeyError:
            raise Exception(
                "Invalid config string for hparms.create_folder_parm: `{folder_config}` not found"
            )
        parm_data = {**parm_data, **folder_settings}
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if child_parm_data:
        parm_data["_children"] = [parm_data for parm_data in child_parm_data]
    if as_data:
        return parm_data
    return create_parm(parm_data)


def create_multiparm_template(
    name: str,
    label: str,
    child_parm_data: Optional[list] = None,
    as_data=False,
    **kwargs,
):
    # Create the multiparm folder
    parm_data = {
        "type": hou.FolderParmTemplate,
        "name": name,
        "label": label,
        "default_value": 1,
        "folder_type": hou.folderType.MultiparmBlock,
    }
    if kwargs:
        parm_data = {**parm_data, **kwargs}
    if child_parm_data:
        parm_data["_children"] = [parm_data for parm_data in child_parm_data]
    if as_data:
        return parm_data
    return create_parm(parm_data)


def is_multiparm(parm: hou.Parm):
    if type(parm) == hou.Parm:  # is a 'real' parm, not a template
        parm_template = parm.parmTemplate()  # Get the parm template
    else:  # Is already a template
        parm_template = parm
    if (
        parm_template.type() == hou.parmTemplateType.Folder
        and not parm_template.isActualFolder()
    ):
        return True
    return False


def is_parm_hidden(parm: hou.Parm):
    # TODO finish this (doesn't work right now...)
    """Extend the default parm.isVisible() functionality to include a check if the parm
    is hidden due to a parent folder being hidden

    Args:
        parm (hou.Parm): The parameter to check the visibility of.

    Returns:
        bool: Whether the parameter is hidden in the Parameter
        interface.
    """
    is_hidden = False

    if not parm.isVisible():
        is_hidden = True
    # If the parm itself is not marked invisible, check parent folders to see if any of
    # those are hidden

    # TODO currently this doesn't work for parms that are inside of folders inside of
    # PLan:
    # from Node, getContainingFolders
    # from Node, get ptg
    # from ptg, find containing folder
    # use ptg is_folder_hidden to check for parent folder's visibility
    # ---
    # ptg = parm.node().parmTemplateGroup()
    # containing_folders = parm.containingFolders()
    # parent_multiparm = parm.parentMultiParm()
    # print("")
    # print(f"parm({parm.name()}) got:")
    # print(f"\tis_hidden: {is_hidden}")
    # print(f"\tcontaining_folders: {containing_folders}")
    # if containing_folders:
    # folder_parm = ptg.findFolder(containing_folders)
    # print(f"\tcontaining_folders parm: {folder_parm.name()}")
    # print(f"\tparent_multiparm: {parent_multiparm}")
    # print("ptg?: ", ptg)

    return is_hidden


def set_folder_parms(
    node: hou.Node, folder_label: Tuple[str, str], new_parms: List[hou.Parm]
):
    ptg = node.parmTemplateGroup()
    existing_fldr = ptg.findFolder(folder_label)
    # print("existing_fldr: ", existing_fldr)
    if not existing_fldr:
        # TODO missing folder exception
        raise Exception(
            f"set_folder_parms could not find folder label '{folder_label}' on node '{node.name()}'"
        )
    parms_tuple = tuple(new_parms)
    new_fldr_parm = hou.FolderParmTemplate(
        existing_fldr.name(),
        existing_fldr.label(),
        parms_tuple,
        folder_type=existing_fldr.folderType(),
        tags=existing_fldr.tags(),
    )
    # existing_fldr.setParmTemplates(parms_tuple)
    # Update parms in template group
    # for new_parm in new_parms:
    # fldr_parm.addParmTemplate(new_parm)

    # Push changes to node
    # Note: Does not change values if the parm already exists
    # (but will change the 'default value' of that parm)
    ptg.replace(existing_fldr.name(), new_fldr_parm)
    # existing_fldr.setParmTemplates(new_parms)
    node.setParmTemplateGroup(ptg)


def disable_all_parms_in_folder(node, folder_name: str):
    # TODO
    print("TODO: Disable parms in a folder")
    node.getFolder()


def disable_parms(node, parms: List, disabled=True):
    # print(f"Disabling parms on: {node.path()}")
    for parm in parms:
        print(f"Disabling parm: ({type(parm)=})")

        if isinstance(parm, hou.FolderParmTemplate):
            # If this is a FolderParmTemplate, we need to 'unpack it' to get the individual parms.
            # Then call this function recursively.
            print(f"Found folder parm: {parm.name()}")
            individual_parms = parm.parmTemplates()
            print(f"Containing {len(individual_parms)} parms")
            disable_parms(node, individual_parms)
            continue

        # node_parm = node.parm(parm.name())
        node_parm = node.parmTuple(parm.name())
        if node_parm:
            # print("locking parm: ", node_parm)
            # For some reason couldn't get parm.disable() to reflect in the UI
            # But lock works well for this case.
            node_parm.lock(disabled)
            # node_parm.disable(True)
        else:
            print(f"WARNING: Unable to disable, parm not foun: {parm.name()}")
            # raise Exception(
            #     "Unable to find expected parm: {}".format(parm.name())
            # )


def reset_parms_to_default(node: hou.Node, folder_name_tuple: Tuple[str, ...]):
    if not isinstance(folder_name_tuple, tuple):
        folder_name_tuple = (folder_name_tuple,)
    print(f"Setting values in {folder_name_tuple}: ")
    # node.parmTuple("cstock_user_color2_0").set((0.5, 0.5, 0.5))
    # Note: parmsInFolder (or parmTuplesInFolder) uses Label and NOT internal name
    # See docs for example usage
    # TODO check if folders exist on HDA, create if missing?
    try:
        existing_parms = node.parmsInFolder(folder_name_tuple)
    except hou.OperationFailed as e:
        print(f"parmsInFolder '{folder_name_tuple}' failed: {e}")
        # print("No existing parms found")
        existing_parms = []
    for parm in existing_parms:
        node.parm(parm.name()).revertToDefaults()
        value = node.parm(parm.name()).eval()
        print(
            "    Reverted {} to default value: {}".format(parm.name(), value)
        )


def all_nodes():
    nodes = hou.node("/").allSubChildren()
    return nodes


def get_dependant_nodes(node):
    """Returns all nodes that reference the target node"""
    print(f"Got dependents for node {node}: ")
    dependents = node.dependents()
    for dependant_node in dependents:
        print("\t", dependant_node)
    if not dependents:
        print("\t(None Found)")
    return dependents


def update_referencing_parms(node: hou.Node):
    # TODO make updates recursive? (in case parms are referencing the updated parm)
    print("")
    print(f"Evaluating {node.path()} referencing parms with parm.eval():")
    referencing_parms = node.parmsReferencingThis()
    print(f"Got {len(referencing_parms)} referencing parms.")

    # all_parms = node.parms()
    print(f"Got {len(referencing_parms)} referencing parms.")
    # print("referecing_parms: ", referencing_parms)
    for parm in referencing_parms:
        # print(f"Got parm: {parm}")
        evaluated_to = parm.eval()
        print("\t", parm, " : ", evaluated_to)
        references = parm.getReferencedParm()
        # evaluated_to = hou.evalParm(parm.path())
        print(f"\t\treferences: {references}")

    print("Cooking nodes: ")
    nodelist = []
    for parm in referencing_parms:
        parmnode = parm.node()
        if parmnode not in nodelist:
            parm.node().cook(force=True)
            print("Cooked: ", parmnode)
            nodelist.append(parmnode)
