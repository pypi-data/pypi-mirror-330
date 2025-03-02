import customtkinter
from project_input import FrameProjectInput
from typing import List
from typing import Optional
from pathlib import Path

import ceonstock
from ceonstock import CstockProjectInput
from ceonstock import CstockProject
from ceonstock import CstockRenderPipeline
from ceonstock import json_io

DEFAULT_JOB_INPUT_TYPE = CstockProjectInput.job_input_types.IMG
DEFAULT_WEB_INPUT_TYPE = CstockProjectInput.web_input_types.IMG


class FrameProjectInputs(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        # self.project_inputs: List[CstockProjectInput] = []
        # self.project_input_frames: List[FrameProjectInput] = []

    def add_project_input(self):
        print("Adding new poroject input")
        new_inputs = self.get()
        new_inputs.append(
            # TODO allow CstockProjectInput to be initialized without web_input_type.
            # Move logic for getting valid web_input_types to cstock module.
            CstockProjectInput(
                name="new_proj_input",
                job_input_type=DEFAULT_JOB_INPUT_TYPE,
                web_input_type=DEFAULT_WEB_INPUT_TYPE,
                description="Describe the project input",
            )
        )
        self.update_project_inputs(new_inputs)

    # def remove_project_input(self):
    #     print("Removing last poroject input")
    #     new_inputs = self.project_inputs[:-1]
    #     self.update_project_inputs(new_inputs)
    #     self.project_inputs = new_inputs

    def get(self) -> List[CstockProjectInput]:
        print("Getting project inputs from UI ...")
        return [frame.get() for frame in self.winfo_children()]

    def update_project_inputs(
        self, new_project_inputs: List[CstockProjectInput]
    ):
        print("Updating UI")
        # Fetch the new list
        # TODO get current inputs from widgets/frames procedurally.
        # Do not store cstock_objects in the variable.
        original_inputs = self.get()
        new_inputs = new_project_inputs

        # Store the length of the current list and the new list
        cur_len, new_len = len(original_inputs), len(new_inputs)
        print(f"{cur_len=}")
        print(f"{new_len=}")

        # If the length of new list is more than current list then
        if new_len > cur_len:
            diff = new_len - cur_len

            # Change text of existing widgets
            for idx, wid in enumerate(self.winfo_children()):
                # wid.config(text=new_items[idx])
                print("TODO apply change")

            # Make the rest of the widgets required
            for i in range(diff):
                print("Adding new pojrect_input widget set.")
                # Button(items_frame, text=new_items[cur_len+i]).pack()
                row = cur_len + i
                cstock_project_input = new_inputs[row]
                # print(f"{row=}")
                new_frame = FrameProjectInput(self, cstock_project_input)
                new_frame.grid(row=row, column=0, pady=(0, 20), sticky="ew")
                # self.project_input_frames.append(new_frame)

        # If the length of current list is more than new list then
        elif new_len < cur_len:
            extra = cur_len - new_len

            # Change the text for the existing widgets
            for idx in range(new_len):
                wid = self.winfo_children()[idx]
                print("TODO apply changes on existing")
                # wid.config(text=new_items[idx])

            # Get the extra widgets that need to be removed
            extra_wids = [
                wid for wid in self.winfo_children()[-1 : -extra - 1 : -1]
            ]  # The indexing is a way to pick the last 'n' items from a list

            # Remove the extra widgets
            for wid in extra_wids:
                wid.destroy()

            # Also can shorten the last 2 steps into a single line using
            # [wid.destroy() for wid in items_frame.winfo_children()[-1:-extra-1:-1]]

        # self.project_inputs = (
        #     new_inputs  # Update the value of the main list to be the new list
        # )


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.version = ceonstock.__version__
        print(self.version)
        self.title(f"CeonStock Project Maker - v{self.version}")
        self.geometry("800x620")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_project_inputs = FrameProjectInputs(self)
        self.frame_project_inputs.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

        # Add button
        self.button_add_input = customtkinter.CTkButton(
            self,
            text="+ Project Input",
            command=self.frame_project_inputs.add_project_input,
        )
        self.button_add_input.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

        # Save/Export
        self.button_export = customtkinter.CTkButton(
            self, text="Export", command=self.export_callback
        )
        self.button_export.grid(
            row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )

    def export_callback(self):
        print("Button Clicked!")
        project_inputs = self.frame_project_inputs.get()
        print(project_inputs)
        file = Path("./ceonstock_project_test.json")
        print("Making file: ", file)
        print(f"Project inputs ({len(project_inputs)}): ")
        render_pipeline = CstockRenderPipeline([], "")
        project = CstockProject(
            project_inputs=project_inputs, render_pipeline=render_pipeline
        )
        for project_input in project_inputs:
            print(project_input)
        # json_io.file_handler.write_json_file(
        #     {"project_inputs": project_inputs}, file
        # )
        json_io.file_handler.write_json_file(project.__dict__, file)
        # with open(file, "w") as f:
        #     f.write("testdata")


# TODO bug:
# After deleting, then creating a new input, the number of inputs is incorrect.
if __name__ == "__main__":
    app = App()
    print(
        "WARNING: TODO FIx bug when deleting and then creating a new input (leaves overwritten input as existing)"
    )
    app.mainloop()
