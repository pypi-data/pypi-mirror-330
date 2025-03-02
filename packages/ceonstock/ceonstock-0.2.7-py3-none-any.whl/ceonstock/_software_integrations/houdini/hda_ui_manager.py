#
# Master interface for functions which are called from within the houdini HDA
#
# Handles the import/export of parms.
# Determines from where to read the in/out files.
# Handles node parm organisation with folders/groups.
# Does not handle parm generataion. Parm generation is handled by the parm_maker.
#
from pprint import pprint
from typing import List
import importlib

import hou
from ceonstock import CstockJobInput
from ceonstock import CstockJob

# from ceonstock.log import printify
# from ceonstock.json_io import cstock_from_json
from ceonstock import json_io

from . import parm_maker

importlib.reload(parm_maker)
importlib.reload(parm_maker.hparms)


class HoudiniHDA:
    """
    Interface for interacting with the houdini HDA node.
    This is the only thing that should need to be imported into Hou.
    -
    Note: For development, it may be necessary to reload submodules inside of houdini with
    importlib.reload(module)
    -
    """

    def __init__(self, node: "hou.Node"):
        self.node = node
        self.job_inputs_import_fldr = ("Imports",)

    def _recook_scene(self):
        print("Recooking Scene ..")
        for node in parm_maker.hparms.all_nodes():
            print(f"\tCooking {node.path()}")
            try:
                node.cook(force=True)
            except Exception:
                print(f"WARNING: Failed to cook node: {node}")

    def _imported_parms(self):
        """Return all parms in the target import folder"""
        imported_parms = self.node.parmsInFolder(self.job_inputs_import_fldr)
        print(
            f"Got import parms from folder '{self.job_inputs_import_fldr}': "
        )
        for parm in imported_parms:
            print(f"\t{parm.name()}: {parm.eval()}")
        if not imported_parms:
            print("\t(None Found)")
        return imported_parms

    def _set_imported_parm_values_to_default(self):
        print(f"Setting parm values to new defaults...")
        imported_node_parms = self.node.parmsInFolder(
            self.job_inputs_import_fldr
        )
        for parm in imported_node_parms:
            parm.revertToDefaults()

    def _apply_parms(self, parms: List[hou.FolderParmTemplate]):
        """Handles applying/updating the given parms to the node."""
        # just to print the parms for testing
        self._imported_parms()

        print("Received list of FolderPartmTemplates to apply:")
        for parm in parms:
            print(f"\t{parm}")

        print(f"Applying {len(parms)} folderParmTemplates to node ...")
        parm_maker.hparms.set_folder_parms(
            self.node, self.job_inputs_import_fldr, parms
        )
        print("Applied parms!")

        # Just printing for debugging
        self._imported_parms()

        # Just to print for debugging.
        parm_maker.hparms.get_dependant_nodes(self.node)

    def import_job_inputs(self, ceonstock_job_json_filepath: str):
        """Import job_inputs from a file and display them as locked nodes.
        inputs:
            node: Assumed to be the Ceonstock HDA which is calling this function.
            ceonstock_job_json_filepath: The filepath to a valid ceonstock_job.json file which includes
        'job_inputs' as a top level key"""
        print(f"Got job_inputs_json_file: {ceonstock_job_json_filepath}")
        print("Reading json file ...")
        cstock_job = json_io.job.from_file(ceonstock_job_json_filepath)
        job_inputs = cstock_job.job_inputs
        print("Got job_inputs:")
        pprint(job_inputs)
        folders_with_parms = []
        print("")
        print("Creating job input parms ... ")
        for job_input in job_inputs:
            job_input_parms = parm_maker.job_input_parms(job_input)
            print("Created new job_input_parms: ")
            for job_input_parm in job_input_parms:
                print(f"\t{job_input_parm}")

            # Wrap each individual job_inut in a folder
            folder_parm = parm_maker.hparms.create_folder_parm(
                job_input.name, job_input.name
            )
            folder_parm.setParmTemplates(job_input_parms)
            folder_parm.setFolderType(hou.folderType.Simple)
            # folder_parm.setFolderType(hou.folderType.Collapsible)
            folders_with_parms.append(folder_parm)

            # Apply and disable
            # _apply_parms(node, [folder_parm])
            # parm_maker.hparms.disable_parms(node, job_input_parms)
        print("")
        self._apply_parms(folders_with_parms)
        # Applying parms will NOT change the values if the parm already exists.
        # Therefore we need to set the values to match the new defaults.
        self._set_imported_parm_values_to_default()
        # For some reason when disabling parms, the UI doesn't update correctly on re-import.
        # Even when un-disabling before applying
        # parm_maker.hparms.disable_parms(node, folders_with_parms, disabled=False)
        # _apply_parms(node, folders_with_parms)
        # parm_maker.hparms.disable_parms(node, folders_with_parms)
