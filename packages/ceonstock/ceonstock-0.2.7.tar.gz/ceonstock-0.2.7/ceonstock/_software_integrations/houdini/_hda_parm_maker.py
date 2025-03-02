from abc import ABC, abstractmethod

import hou

import ceonstock.integrations.hou.hparms as hparms
import ceonstock.integrations.hou.type_parms as tp
import ceonstock.integrations.hou.hda_parm_namer as parm_namer
import ceonstock.core.proj_input_type as cprojtype
import ceonstock.core.proj_input as cprojinput
import ceonstock.core.job_input as cjobinput
import ceonstock.utility as helper

if False: # To prevent flake8 from failing on the string type-hints during CI
    from ceonstock.core.base import CstockBaseEnum


class IHouParmGroup(ABC):
    @abstractmethod
    def parm_templates(self) -> list:
        """returns the parms as a list of parm_templates"""
        pass

    @abstractmethod
    def parm_data(self) -> list:
        """returns the parms as a list of parm_data objects"""
        pass


class TestInputParmGroup(IHouParmGroup):
    def __init__(self, proj_input: cprojinput.CstockProjInput):
        self.proj_input = proj_input
        self.proj_input_type = proj_input.proj_input_type
        self.parm_name = f"test_{proj_input.name}"

    def parm_templates(self) -> list:
        # parmTemplate = self.create_type_picker_dropdown()
        # type_picker = self.create_type_picker_dropdown()
        print("\n\n---Creating parm_templates---")
        parm_templates = [
            hparms.create_parm(parm_data) for parm_data in self.parm_data(debug=True)
        ]
        helper.cprint(parm_templates, f"Created parm_templates:")
        # parms.append(type_picker)
        # parm_templates.append(hparms.create_parm(self.parm_data()))
        return parm_templates

    def parm_data(self, debug=False) -> list:
        input_info_parms = self.input_info_parms()
        value_entry_parms = self.value_entry_parms()
        parm_data = [*input_info_parms, *value_entry_parms]
        if debug:
            helper.cprint(parm_data, "hda_parm_maker created parm_data: ")
        return parm_data

    def value_picker(self) -> list:
        """Takes the proj_input_type
        returns parm data of the appropriate type"""
        class_lookup = {
            cprojtype.CstockProjInputType.AUDIO: tp.TypeParmFile,
            cprojtype.CstockProjInputType.COLOR: tp.TypeParmColor,
            cprojtype.CstockProjInputType.DOC: tp.TypeParmFile,
            cprojtype.CstockProjInputType.DROPDOWN: tp.TypeParmDropdown,
            cprojtype.CstockProjInputType.IMG: tp.TypeParmImg,
            cprojtype.CstockProjInputType.INT: tp.TypeParmInt,
            cprojtype.CstockProjInputType.TEXT: tp.TypeParmString,
        }
        cls_type_parm = class_lookup[self.proj_input_type]
        parm_datas = cls_type_parm(
            self.parm_name, self.proj_input.type_settings
        ).value_picker()
        return parm_datas

    def input_info_parms(self) -> list:
        heading = hparms.create_heading_parm(
            f"{self.parm_name}_heading",
            f"{self.parm_name}_label",
            f"{self.parm_name}_text",
            as_data=True,
        )
        job_input_name = hparms.create_label_parm(
            f"{self.parm_name}_name",
            f"job input name: ",
            f"{self.proj_input.name}",
            tags={"cstock_attrib": "name"},
            as_data=True,
        )
        job_input_type = hparms.create_label_parm(
            f"{self.parm_name}_type",
            f"job input type: ",
            f"{self.proj_input.job_input_type().value}",
            tags={"cstock_attrib": "job_input_type"},
            as_data=True,
        )
        label_description_text = hparms.create_message_parm(
            f"{self.parm_name}_description_text",
            "Description",
            text=self.proj_input.description,
            tags={"cstock_attrib": "description"},
            as_data=True,
        )
        return [heading, job_input_type, job_input_name, label_description_text]

    def value_entry_parms(self) -> list:
        entry_metadata_fldr = {
            "type": hou.FolderParmTemplate,
            "name": f"{self.parm_name}_fldr_information",
            "label": "Metadata",
            "folder_type": hou.folderType.Collapsible,
            "_children": [
                hparms.create_message_parm(
                    f"{self.parm_name}_metadata_help",
                    "",
                    text=(
                        "Available metadata for this input entry.\n"
                        "Note: Some metadata cannot be generated in Houdini, but "
                        "will be available for use in production.\n"
                        "Metadata is not yet implemented"
                    ),
                    as_data=True,
                ),
            ],
        }
        multiparm = {
            **hparms.create_multiparm_template(
                self.parm_name,
                self.parm_name,
                as_data=True,
            ),
            "_children": self.value_picker(),
        }
        sepparm = {
            "type": hou.SeparatorParmTemplate,
            "name": f"sepparm_end_of_{self.parm_name}",
        }
        return [*self.value_picker(), entry_metadata_fldr, sepparm]


class ProjInputParmGroup(IHouParmGroup):
    def parm_templates(self):
        # parmTemplate = self.create_type_picker_dropdown()
        # type_picker = self.create_type_picker_dropdown()
        parm_templates = []
        # parms.append(type_picker)
        parm_templates.append(hparms.create_parm(self.parm_data()))
        # print("proj input editor UI parm_template() returned: ", parms)
        return parm_templates

    def parm_data(self):
        parm_data = {
            **hparms.create_multiparm_template(
                parm_namer.ParmNamer.PROJ_INPUT.BASE_MULTIPARM,
                "Project Inputs",
                as_data=True,
            ),
            "_children": [
                *self.type_picker_parm(),
                *self.common_parms(),
                *self.create_type_settings(),
                {
                    "type": hou.SeparatorParmTemplate,
                    "name": f"sepparm_end_of_type_settings_#",
                },
            ],
        }
        return parm_data

    def type_picker_parm(self):
        # Get dropdown options
        dropdown_options = []
        for input_type in cprojtype.CstockProjInputType:
            dropdown_options.append(
                {"value": input_type.value, "label": input_type.value}
            )
        # Create parm data
        dropdown_parm_data = hparms.create_dropdown_parm(
            "proj_input_#_type",
            "Input Type",
            dropdown_options,
            tags={"cstock_attrib": "proj_input_type"},
            as_data=True,
        )
        return [dropdown_parm_data]

    def common_parms(self):
        # Parms that will be necessary for every proj_input, regardless of type
        # Returns a list of dictionaries containing parm_data
        label_name_parm_data = hparms.create_heading_parm(
            "proj_input_#_label_name",
            "Show Name",
            text=f'`chs("proj_input_#_name")',
            as_data=True,
        )

        common_properties_parm_data = {
            "type": hou.FolderParmTemplate,
            "name": "proj_input_#_fldr_information",
            "label": "Input Information",
            "folder_type": hou.folderType.Collapsible,
            "_children": [
                hparms.create_text_parm(
                    "proj_input_#_name",
                    "Input Name",
                    tags={"cstock_attrib": "name"},
                    default_value="proj_input_#",
                    as_data=True,
                ),
                hparms.create_toggle_parm(
                    "proj_input_#_required",
                    "Required",
                    tags={"cstock_attrib": "required"},
                    default_value=True,
                    as_data=True,
                ),
                hparms.create_text_parm(
                    "proj_input_#_description",
                    "Input Description",
                    tags={"cstock_attrib": "description"},
                    multiline=True,
                    as_data=True,
                ),
            ],
        }
        return [label_name_parm_data, common_properties_parm_data]

    def create_type_settings(self):
        # Parms that are necessary only for each specific input type
        parms = []
        for input_type in cprojtype.CstockProjInputType:
            name = f"proj_input_#_type_settings_{input_type.value}"
            label = f"{input_type.value} settings"
            _children = ProjInputTypeSettings(input_type).parm_templates()
            # TODO show only if current input_type == this input type
            type_settings_parm_data = {
                "type": hou.FolderParmTemplate,
                "name": name,
                "label": label,
                "folder_type": hou.folderType.Collapsible,
                "conditionals": {
                    hou.parmCondType.HideWhen: f"{{ proj_input_#_type != {input_type.value}}}"
                },
                "_children": _children,
            }
            parms.append(type_settings_parm_data)
        return parms


# TODO refactor, move this to type_parms?
class ProjInputTypeSettings:
    # A map of required type_settings and the relevant parm_type to create.
    TYPE_SETTING_PARMS = {
        cprojtype.CstockProjInputType.DROPDOWN: [
            {
                "type_setting": "dropdown_options",
                "parm_function": hparms.create_multiparm_template,
                "parm_kwargs": {
                    "tags": {"cstock_attrib": "type_settings.dropdown_options"},
                    "child_parm_data": [
                        hparms.create_text_parm(
                            name="proj_input_#_type_setting_dropdown_option_#_label",
                            label="Label",
                            tags={"cstock_attrib": "label"},
                            help="The text that will be shown on the dropdown menu",
                            join_with_next=True,
                            as_data=True,
                        ),
                        hparms.create_text_parm(
                            name="proj_input_#_type_setting_dropdown_option_#_value",
                            label="Value",
                            tags={"cstock_attrib": "value"},
                            help="The value received by the software if the user chooses this option",
                            as_data=True,
                        ),
                        {
                            "type": hou.SeparatorParmTemplate,
                            "name": "proj_input_#_type_settings_dropdown_options_#_sepparm",
                        },
                    ],
                },
            }
        ]
    }
    """ Generate parms for specific proj input types """

    def __init__(self, proj_input_type: cprojtype.CstockProjInputType):
        print("Create ProjInputTypeSettings with proj_input_type: ", proj_input_type)
        self.input_type = proj_input_type

    def parm_templates(self):
        parm_templates = []
        # Use a factory-like pattern to build the relevant parm templates
        print("self.input_type: ", self.input_type)
        type_setting_parms = self.TYPE_SETTING_PARMS.get(self.input_type)
        if not type_setting_parms:
            return []
        for type_setting_parm in type_setting_parms:
            type_setting = type_setting_parm["type_setting"]
            parm_func = type_setting_parm["parm_function"]
            type_kwargs = type_setting_parm["parm_kwargs"]

            # setup parm data to create the type_settings folder
            name = f"proj_input_#_type_setting_{self.input_type.value}_{type_setting}"
            label = f"{type_setting}"

            # Append additional kwargs to type_settings folder
            hide_condition = f"{{ proj_input_#_type != {self.input_type.value}}}"
            conditionals = {"conditionals": {hou.parmCondType.HideWhen: hide_condition}}
            type_kwargs = {
                **type_kwargs,
                **conditionals,
            }

            # Append additional kwargs to all children parms inside the folder
            common_child_kwargs = conditionals
            child_parm_data = type_kwargs["child_parm_data"]
            new_child_parm_data = [
                {**child_parm, **common_child_kwargs} for child_parm in child_parm_data
            ]
            type_kwargs["child_parm_data"] = new_child_parm_data

            # Generate the parm_data
            parm_data = parm_func(name, label, **type_kwargs, as_data=True)
            parm_templates.append(parm_data)
        return parm_templates


class JobInputParmGroup(IHouParmGroup):
    def __init__(self, job_input: cjobinput.CstockJobInput):
        self.job_input = job_input

    def parm_template(self):
        parm_templates = []
        parm_templates.append(hparms.create_parm(self.parm_data()))
        return parm_templates

    def parm_data(self):
        parm_data = {
            **hparms.create_multiparm_template(
                parm_namer.ParmNamer.JOB_INPUT.BASE_MULTIPARM,
                "Job Inputs",
                as_data=True,
            ),
            "_children": [
                *self.common_parms(),
            ],
        }
        return parm_data

    def common_parms(self):
        # Parms that will be necessary for every proj_input, regardless of type
        # Returns a list of dictionaries containing parm_data
        input_entry_metadata_parm_data = {
            "type": hou.FolderParmTemplate,
            "name": "job_input_#_fldr_metadata",
            "label": "Input Information",
            "folder_type": hou.folderType.Collapsible,
            "_children": [
                hparms.create_text_parm(
                    "job_input_#_name",
                    "Input Name",
                    tags={"cstock_attrib": "name"},
                    default_value="job_input_#",
                    as_data=True,
                ),
                hparms.create_text_parm(
                    "job_input_#_value",
                    "Input Description",
                    # tags={"cstock_attrib": "value"},
                    multiline=True,
                    as_data=True,
                ),
            ],
        }
        return [input_entry_metadata_parm_data]
