import logging
from ceonstock import CstockProject
from ceonstock import CstockProjectInput
from ceonstock import CstockJob
from ceonstock import CstockJobInputType
from ceonstock import CstockWebInputType
from ceonstock.core.project import CstockProjectInfo
from ceonstock.core.project import CstockRenderPipeline
from ceonstock.log import printify

from ceonstock.job_maker import project_preview_video_maker
from ceonstock.job_maker import job_maker

from ceonstock.log import formatters, formats

root_logger = logging.getLogger()
root_logger.setLevel("INFO")

formatter = formatters.ColoredFormatter(formats.DEV)
sh = logging.StreamHandler()
sh.setFormatter(formatter)

root_logger.addHandler(sh)

logger = logging.getLogger(__name__)

PROJECT_INPUT_PREVIEW_FILES_DIR_DEFAULT = "/mnt/FileStorage/Dayne/Web/proj_ceonstock/assets/project_input_files/project_preview_video_inputs/default_inputs"
PROJECT_INPUT_PREVIEW_FILES_DIR_EXAMPLES = "/mnt/FileStorage/Dayne/Web/proj_ceonstock/assets/project_input_files/project_preview_video_inputs/example_inputs"
JOBS_DIR = "/mnt/FileStorage/Dayne/Web/proj_ceonstock/local_storage/jobs"

# PROJECT_INPUTS = [
#     CstockProjectInput(
#         name="pen_color",
#         job_input_type=CstockJobInputType.COLOR,
#         web_input_type=CstockWebInputType.COLOR,
#         description="Color of pen",
#     ),
#     CstockProjectInput(
#         name="flag_image",
#         job_input_type=CstockJobInputType.IMG,
#         web_input_type=CstockWebInputType.IMG,
#         description="Image on flag",
#     ),
#     CstockProjectInput(
#         name="box_color",
#         job_input_type=CstockJobInputType.COLOR,
#         web_input_type=CstockWebInputType.COLOR,
#         description="Color of box",
#     ),
# ]
PROJECT_INPUTS = [
    CstockProjectInput(
        name="single_image",
        job_input_type=CstockJobInputType.IMG,
        web_input_type=CstockProjectInput.web_input_types.IMG,
        description="A single image TODO system to enforce limit on num inputs",
    ),
    CstockProjectInput(
        name="image_from_doc",
        job_input_type=CstockJobInputType.IMG,
        web_input_type=CstockProjectInput.web_input_types.DOC,
        description="A single image TODO system to enforce limit on num inputs",
    ),
    CstockProjectInput(
        name="single_color",
        job_input_type=CstockJobInputType.COLOR,
        web_input_type=CstockProjectInput.web_input_types.COLOR,
        description="A single color",
    ),
    CstockProjectInput(
        name="dropdown_string",
        job_input_type=CstockJobInputType.STRING,
        web_input_type=CstockProjectInput.web_input_types.DROPDOWN,
        type_settings={
            "dropdown_options": [
                {
                    "value": "dropdown_option_value_0",
                    "label": "Option Label 0",
                },
                {
                    "value": "dropdown_option_value_1",
                    "label": "Option Label 1",
                },
                {
                    "value": "dropdown_option_value_2",
                    "label": "Option Label 2",
                },
            ]
        },
        description="A single image TODO system to enforce limit on num inputs",
    ),
]

RENDER_PIPELINE = CstockRenderPipeline(
    render_tasks=[], primary_output="out", extra_outputs=[]
)

PROJECT_INFO = CstockProjectInfo(
    "My Test Project",
    description="Testing the genration of jobs for hte preview video",
    tags=[],
)

PROJECT_TO_TEST = CstockProject(
    project_inputs=PROJECT_INPUTS,
    render_pipeline=RENDER_PIPELINE,
    project_info=PROJECT_INFO,
)


def main(ceonstock_project: CstockProject):
    project_input_jobs: dict[
        str, list[CstockJob]
    ] = project_preview_video_maker.create_jobs_for_project_preview_video(
        ceonstock_project,
        files_dir_default=PROJECT_INPUT_PREVIEW_FILES_DIR_DEFAULT,
        files_dir_examples=PROJECT_INPUT_PREVIEW_FILES_DIR_EXAMPLES,
    )
    print_header("Created project_input jobs:")
    logger.info(f"{printify(project_input_jobs)}")

    # Test execute
    print()
    project_input_name_to_test: str = list(project_input_jobs.keys())[1]
    print_header(
        f"Testing with isolated project input: {project_input_name_to_test}"
    )
    jobs_for_project_input = project_input_jobs[project_input_name_to_test]
    file_sources = [
        PROJECT_INPUT_PREVIEW_FILES_DIR_DEFAULT,
        PROJECT_INPUT_PREVIEW_FILES_DIR_EXAMPLES,
    ]
    for job in jobs_for_project_input:
        logger.info(f"{job}")
        job_maker.create_cstock_job_on_disk(job, JOBS_DIR, file_sources)


def print_header(msg):
    logger.info(f"*****\n{msg}\n*****")


if __name__ == "__main__":
    main(PROJECT_TO_TEST)
