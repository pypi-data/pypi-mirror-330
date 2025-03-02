import hou
from abc import ABC, abstractmethod
from typing import List

import ceonstock.integrations.hou.hparms as hparms
import ceonstock.integrations.hou.parm_processor as pp
import ceonstock.integrations.hou.hda_parm_maker as parm_maker
import ceonstock.integrations.hou.hda_parm_namer as parm_namer
import ceonstock.core.proj_input as cprojinput
import ceonstock.core.job_input as cjobinput
import ceonstock.integrations.hou.exceptions as hou_err
import ceonstock.utility as utility


"""
class MappedParmGroup:
    # TODO move this to multiparm processor? Mostly only necessary when dealing with
    # multiple multiparm instances?

    def __init__(self, object_instance, parm_group):
        # TODO test that passed object instances will correctly updated by reference
        self.object_instance = object_instance
        self.parm_group = parm_group
        self.visible_parms = self.get_visible_parms()
        self.multiparm_handler = mpp.MultiparmProcessorDictKeyFromParmTag(
            "cstock_dict_key"
        )

    def get_visible_parms(self):
        self.parm_group[0].node().updateParmStates()
        visible_parms = [
            parm for parm in self.parm_group if not hparms.is_parm_hidden(parm)
        ]
        self.visible_parms = visible_parms
        return visible_parms

    def set_parms(self):
        for parm in self.parm_group:
            # TODO better way to handle the missing parm problem?
            # From a higher level, first set multiparm instances, then set the values?
            try:
                tags = parm.parmTemplate().tags()
                attrib_name = tags.get("cstock_attrib")
                if not attrib_name:
                    return
                new_value = self.object_instance.to_dict().get(attrib_name)
                if not new_value:
                    print(
                        f"WARNING: Skipping parm({parm.name()}), attrib({attrib_name}) not found in class instance {self.object_instance.__class__}."
                    )
                    return
                print(
                    f"Setting parm({parm.name()}) from attrib({attrib_name}) to new_value: {new_value}"
                )
                hparms.set_parm(
                    parm, new_value, multiparm_processor=self.multiparm_handler
                )
            except hou.ObjectWasDeleted:
                print("WARNING: Skipped deleted parm")

    def from_parms(self):
        print("")
        proj_input_dict = {}
        for parm in self.visible_parms:
            tags = parm.parmTemplate().tags()
            attrib_name = tags.get("cstock_attrib")
            if attrib_name:
                new_value = hparms.read_parm(
                    parm, multiparm_processor=self.multiparm_handler
                )
                proj_input_dict[attrib_name] = new_value
                # print(f"got parm({parm.name()}) value for attrib({attrib_name}): {new_value}")
        # Create object instance
        processed_proj_input_dict = utility.dict_dotnotation_to_nested(proj_input_dict)
        utility.print_dict(
            processed_proj_input_dict, msg="Created processed_proj_input_dict: "
        )
        new_object_instance = self.object_instance.from_dict(processed_proj_input_dict)
        return new_object_instance
"""

"""
def create_mapped_parm_groups(multiparm, object_instances):
    # TODO split into two functions:
    # one for creating new class instances from existing parms.
    # One for creating new parms from existing instances.
    parm_instance_groups = hparms.get_multiparm_parms_grouped_by_instance(multiparm)
    mapped_parm_groups = []

    # If object_instances is not a list, assume a class definition was received
    # Map the parms to the desired class definition instead of an instance
    create_new_instances = False if isinstance(object_instances, list) else True

    for instance_index, parm_group in parm_instance_groups.items():
        instance_to_map = (
            object_instances
            if create_new_instances
            else object_instances[int(instance_index) - 1]
        )
        mapped_parm_group = MappedParmGroup(instance_to_map, parm_group)
        mapped_parm_groups.append(mapped_parm_group)
    return mapped_parm_groups
"""


class IUIManager(ABC):
    @abstractmethod
    def to_parms():
        """Loads the python classes into the houdini UI"""

    @abstractmethod
    def from_parms():
        """Creates new classe by reading the current houdini UI."""


class ProjInputUIManager(IUIManager):
    def __init__(self, node):
        self.node = node
        self.multiparm_name = parm_namer.ParmNamer.PROJ_INPUT.BASE_MULTIPARM
        self.parms_processor = pp.ParmsProcessor(
            pp.ParmProcessorFromParmTag("cstock_attrib")
        )

    def load_proj_input_editor(self):
        proj_input_editor_parms = parm_maker.ProjInputParmGroup().parm_templates()
        print("proj_input_editor_parms: ", proj_input_editor_parms)
        hparms.set_folder_parms(
            self.node,
            parm_namer.ParmNamer.PROJ_INPUT.TARGET_FOLDER,
            proj_input_editor_parms,
        )

    def to_parms(self, proj_inputs: List[cprojinput.CstockProjInput]):
        # Create multiparm parameter instances
        multiparm = self.get_multiparm(self.multiparm_name)
        num_inputs = len(proj_inputs)
        multiparm.set(num_inputs)

        # Map each proj_input object with the corresponding group of parameters
        parm_instance_groups = hparms.get_multiparm_parms_grouped_by_instance(multiparm)
        for index, parms in parm_instance_groups.items():
            proj_input = proj_inputs[int(index) - 1]
            print("Setting parms for proj_input: ", proj_input)
            values_to_set = proj_input.to_dict()
            utility.cprint(values_to_set, "values_to_set: ")
            self.parms_processor.set_values(parms, values_to_set)

    def from_parms(self) -> List[cprojinput.CstockProjInput]:
        """
        Creates proj inputs from current parm settings.
        Returns the new proj_input instances
        """
        multiparm = self.get_multiparm(self.multiparm_name)
        new_proj_inputs = []

        print("")
        parm_instance_groups = hparms.get_multiparm_parms_grouped_by_instance(multiparm)
        for _, parms in parm_instance_groups.items():
            # Filter to remove parms that are hidden from the UI
            filtered_parms = hparms.get_visible_parms(parms)
            values_from_parms = self.parms_processor.get_values(filtered_parms)
            new_proj_input = cprojinput.CstockProjInput.from_dict(values_from_parms)
            new_proj_inputs.append(new_proj_input)
        utility.cprint(new_proj_inputs, msg="proj_inputs after getting from parms: ")
        return new_proj_inputs

    def get_multiparm(self, multiparm_name):
        """Helper function for validating expected multiparms"""
        multiparm = self.node.parm(multiparm_name)
        if not multiparm:
            raise hou_err.MissingParmException(multiparm_name, self.node.path())
        if not multiparm.isMultiParmParent():
            raise Exception(f"Parm({multiparm.name()}) is not a multiparm")
        return multiparm


class TestInputUIManager(IUIManager):
    def __init__(self, node):
        self.node = node
        self.target_folder_name = parm_namer.ParmNamer.TEST_INPUT.TARGET_FOLDER
        self.parms_processor = pp.ParmsProcessor(
            pp.ParmProcessorFromParmTag("cstock_attrib")
        )

    def from_parms(self) -> List[cjobinput.CstockJobInput]:
        target_folder_parm_template = self.node.parmTemplateGroup().findFolder(
            self.target_folder_name
        )
        test_input_folders = hparms.parm_templates_in_folder(
            target_folder_parm_template
        )
        print("Got test_input_folders: ", test_input_folders)
        new_job_inputs = []
        for proj_input_folder in test_input_folders:
            print("Got folder parm: ", proj_input_folder)
            parm_tuples_in_folder = hparms.parm_tuples_in_folder(
                self.node, proj_input_folder
            )
            utility.cprint(parm_tuples_in_folder, "parm_tuples_in_folder: ")

            values_from_parms = self.parms_processor.get_values(parm_tuples_in_folder)
            print("\tCreated values: ", values_from_parms)

            # Make sure that 'values' is a list
            if not isinstance(values_from_parms["values"], list):
                values_from_parms["values"] = [values_from_parms["values"]]

            new_job_input = cjobinput.CstockJobInput.from_dict(values_from_parms)
            print("\tCreated job_input: ", new_job_input)
            new_job_inputs.append(new_job_input)

        utility.cprint(new_job_inputs, msg="job_inputs created from test parms: ")
        return new_job_inputs

    def to_parms(self, proj_inputs: List[cprojinput.CstockProjInput]):
        """
        For each proj_input, create a multiparm.
        Each multiparm instance corresponds to one user entry for this input, and
        includes associated metadata.
        The whole multiparm template will be created according to the job_input type.
        """
        new_parms = []
        for proj_input in proj_inputs:
            fldr_name = f"test_{proj_input.name}_fldr"
            folder_parms = parm_maker.TestInputParmGroup(proj_input).parm_data()
            new_folder = hparms.create_folder_parm(
                fldr_name,
                fldr_name,
                child_parm_data=folder_parms,
                folder_config="collapsible",
                as_data=True,
            )
            new_parm = hparms.create_parm(new_folder)
            new_parms.append(new_parm)
        # Flatten the list
        # new_parms_flatlist = [
        # new_parm for parm_list in new_parms for new_parm in parm_list
        # ]
        utility.cprint(new_parms, "hda_ui_manager to_parms: setting new parms: ")
        hparms.set_folder_parms(
            self.node,
            parm_namer.ParmNamer.TEST_INPUT.TARGET_FOLDER,
            new_parms,
        )


class JobInputUIManager(IUIManager):
    def __init__(self, node, job_inputs=[]):
        self.node = node
        self.job_inputs = job_inputs

    def to_parms(self):
        """
        For each job_input, create a multiparm.
        Each multiparm instance corresponds to one user entry for this input, and
        contains associated metadata.
        The whole multiparm template will be created according to the job_input type.
        """
        imported_job_input_parms = parm_maker.HDAParmMaker().job_input_parms()
        hparms.set_folder_parms(
            self.node,
            parm_namer.ParmNamer.JOB_INPUT.IMPORT_FOLDER,
            imported_job_input_parms,
        )

    def from_parms(self):
        pass

    def from_proj_inputs(self, list_of_proj_inputs):
        new_job_inputs = [
            cjobinput.CstockJobInput.from_proj_input(proj_input)
            for proj_input in list_of_proj_inputs
        ]
        self.job_inputs = new_job_inputs
        return new_job_inputs


class HDAUIManager:
    def __init__(self, node, job_inputs=[]):
        print("Init HDAUIManager! node: ", node)
        # TODO refactor: the UI managers should not store inputs, just provide logic
        # to set and fetch from/to parms.
        # Only the HDAUIManager handles the proj/job inputs
        self.node = node
        self.proj_inputs = ProjInputUIManager(node)
        self.test_inputs = TestInputUIManager(node)
        self.job_inputs = JobInputUIManager(node, job_inputs)
        # TODO pipeline

    def get_proj_inputs(self):
        return self.proj_inputs.from_parms()

    def import_test_inputs(self):
        # self.proj_inputs.from_parms()
        proj_inputs = self.proj_inputs.from_parms()
        self.test_inputs.to_parms(proj_inputs)
        print("test inputs to parms:")
        for proj_input in proj_inputs:
            print("test_input: ", proj_input)

    # def export_test_inputs(self):
    # job_inputs = self.job_inputs.from_parms()
    # print("TODO export job_inputs: ")
    # for job_input in job_inputs:
    # print(job_input)
