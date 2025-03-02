from pathlib import Path

from ceonstock.log import logging_info, module_logger, logging_setup, printify
from ceonstock import json_io
from ceonstock import CstockJobInput, CstockProjInput, CstockRenderTask

# Logger setup
logging_setup.setup_root_logger()

logger = module_logger()


if __name__ == "__main__":
    # Testing github changes
    filename = "tempTests/myTestJSON.json"
    print(f"Exporting to: {Path(filename)}")

    # Job Inputs
    job_input1 = CstockJobInput(
        "my_job_input_1", CstockJobInput.types.IMG, values=["relpath/to/somefile.jpg"]
    )
    job_input2 = CstockJobInput(
        "my_job_input_2",
        CstockJobInput.types.IMG,
        values=["relpath/to/someotherfile.jpg"],
    )
    job_inputs = [job_input1, job_input2]

    # Proj Inputs
    proj_input1 = CstockProjInput(
        name="my_proj_input_1",
        job_input_type=CstockProjInput.job_input_types.IMG,
        web_input_type=CstockProjInput.web_input_types.IMG,
    )
    proj_input2 = CstockProjInput(
        name="my_proj_input_2",
        job_input_type=CstockProjInput.job_input_types.IMG,
        web_input_type=CstockProjInput.web_input_types.IMG,
    )
    proj_inputs = [proj_input1, proj_input2]

    # Render Tasks
    render_task1 = CstockRenderTask(
        name="my_render_task",
        app_type=CstockRenderTask.app_types.HOU,
        app_version="19.5",
        target_file="relpath/to/file.hiplc",
        output="render_output.$F4.exr",
        app_render_settings={},
    )
    render_task2 = CstockRenderTask(
        name="my_render_task2",
        app_type=CstockRenderTask.app_types.HOU,
        app_version="19.5",
        target_file="relpath/to/file.hiplc",
        output="render_output.$F4.exr",
        app_render_settings={},  # TODO target node, render engine etc
    )
    render_tasks = [render_task1, render_task2]

    # Export
    dict_data = {
        "proj_inputs": proj_inputs,
        "render_tasks": render_tasks,
        "job_inputs": job_inputs,
    }
    json_io.write_json_file(dict_data, filename)

    print(f"Loading from file: {filename}")
    loaded_data = json_io.read_json_file(filename)
    print(printify(loaded_data))
