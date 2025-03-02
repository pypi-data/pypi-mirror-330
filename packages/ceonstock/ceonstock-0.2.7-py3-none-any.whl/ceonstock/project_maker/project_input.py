# The UI for setting up a single project input.
import customtkinter
import tkinter
from ceonstock import CstockJobInputType
from ceonstock import CstockWebInputType
from ceonstock import CstockProjectInput
from typing import List
from typing import Optional


def dropdown_callback(arg):
    print(arg)


def valid_ui_types(
    job_input_type: CstockJobInputType,
) -> List[CstockWebInputType]:
    LOOKUP = {
        CstockJobInputType.AUDIO: [CstockWebInputType.AUDIO],
        CstockJobInputType.COLOR: [CstockWebInputType.COLOR],
        # CstockJobInputType.FLOAT: [CstockWebInputType.FLOAT], # TODO add float webinput?
        CstockJobInputType.IMG: [
            CstockWebInputType.IMG,
            CstockWebInputType.DOC,
        ],
        CstockJobInputType.INT: [CstockWebInputType.INT],
        CstockJobInputType.STRING: [CstockWebInputType.TEXT],
    }
    return LOOKUP[job_input_type]


LABEL_STICKY = "e"


def test_callback(value):
    print(value)


def format_project_name(value):
    """Format the name according to requirements"""
    out_value = value
    out_value = out_value.replace(" ", "_")
    out_value = out_value.lower()
    # print("out: ", out_value)
    return out_value


default_project_input = CstockProjectInput(
    name="Unnamed Project Input",
    job_input_type=CstockJobInputType.IMG,
    web_input_type=CstockWebInputType.IMG,
)


class FrameProjectInput(customtkinter.CTkFrame):
    def __init__(
        self, master, cstock_project_input: Optional[CstockProjectInput] = None
    ):
        super().__init__(master)
        # self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0)
        self.grid_columnconfigure(1, weight=2)

        if not cstock_project_input:
            cstock_project_input = default_project_input

        print("Creating frame with cstock_project_input: ")
        print(cstock_project_input)

        # Label shown in the UI
        self.title = customtkinter.CTkLabel(
            self,
            text=cstock_project_input.name,
            fg_color="gray30",
            font=("", 18),
            corner_radius=6,
        )
        self.title.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=2
        )
        # Delete button
        self.button_delete = customtkinter.CTkButton(
            self,
            width=30,
            text="X",
            fg_color="#a44",
            font=("", 18),
            command=self.destroy,
        )
        self.button_delete.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )

        def on_name_change(*args):
            value = f"{self.entry_job_input_name.get()}"
            value = format_project_name(value)
            self.title.configure(text=value)
            # print(f"{value=}")

        # Project Input Name
        row = 1
        self.label_job_input_name = customtkinter.CTkLabel(
            self, text="Project Input Name"
        )
        self.label_job_input_name.grid(
            row=row, column=0, padx=(20, 0), sticky=LABEL_STICKY
        )
        # Use a variable to trigger onchange callback
        self.name_var = tkinter.StringVar()
        self.name_var.trace_add("write", on_name_change)
        self.entry_job_input_name = customtkinter.CTkEntry(
            self, placeholder_text="job_input_name", textvariable=self.name_var
        )
        self.entry_job_input_name.grid(
            row=row, column=1, padx=20, pady=5, sticky="ew"
        )

        # Project Input Description
        row += 1
        self.label_project_input_description = customtkinter.CTkLabel(
            self, text="Project Input Description"
        )
        self.label_project_input_description.grid(
            row=row, column=0, padx=(20, 0), sticky=LABEL_STICKY
        )
        self.textbox_project_input_description = customtkinter.CTkTextbox(
            self, height=76
        )
        self.textbox_project_input_description.grid(
            row=row, column=1, padx=20, pady=5, sticky="ew"
        )

        # Job Input Type
        row += 1
        self.label_job_input_type = customtkinter.CTkLabel(
            self, text="Job Input Type"
        )
        self.label_job_input_type.grid(
            row=row, column=0, padx=(20, 0), sticky=LABEL_STICKY
        )
        options_job_input_type = [e.value for e in CstockJobInputType]
        self.dropdown_job_input_type = customtkinter.CTkOptionMenu(
            self,
            values=options_job_input_type,
            command=self.refresh_web_ui_options,
        )
        self.dropdown_job_input_type.grid(
            row=row, column=1, padx=20, pady=5, sticky="ew"
        )

        # Web Input Type
        row += 1
        self.label_web_input_type = customtkinter.CTkLabel(
            self, text="Web Input Type"
        )
        self.label_web_input_type.grid(
            row=row, column=0, padx=(20, 0), sticky=LABEL_STICKY
        )
        options_web_ui = valid_ui_types(options_job_input_type[0])
        self.dropdown_web_input_type = customtkinter.CTkOptionMenu(
            self,
            values=options_web_ui,
            command=dropdown_callback,
        )
        self.dropdown_web_input_type.grid(
            row=row, column=1, padx=20, pady=5, sticky="ew"
        )

        # Set default values
        self.set(cstock_project_input)

    def refresh_web_ui_options(self, job_input_type_value: str):
        job_input_type = CstockJobInputType(job_input_type_value)
        web_ui_types = valid_ui_types(job_input_type)
        options = [web_ui_type.value for web_ui_type in web_ui_types]
        self.dropdown_web_input_type.configure(values=options)
        self.dropdown_web_input_type.set(options[0])
        if len(options) <= 1:
            self.dropdown_web_input_type.configure(state="disabled")
        else:
            self.dropdown_web_input_type.configure(state="normal")

    def set(self, cstock_project_input: CstockProjectInput):
        # Set values
        self.textbox_project_input_description.insert(
            "0.0", cstock_project_input.description
        )
        self.dropdown_job_input_type.set(
            cstock_project_input.job_input_type.value
        )
        self.name_var.set(cstock_project_input.name)
        self.refresh_web_ui_options(cstock_project_input.job_input_type.value)

    def get(self) -> CstockProjectInput:
        """Build a CstockprojectInput instance from the provided settings in the UI"""
        name = self.entry_job_input_name.get()
        job_input_type = self.dropdown_job_input_type.get()
        web_input_type = self.dropdown_web_input_type.get()
        description = self.textbox_project_input_description.get("0.0", "end")
        description = description.strip()  # Remove trailing newline
        cstock_project_input = CstockProjectInput(
            name,
            job_input_type=job_input_type,
            web_input_type=web_input_type,
            description=description,
        )
        print(name, job_input_type, web_input_type, description)
        print(cstock_project_input)
        return cstock_project_input
