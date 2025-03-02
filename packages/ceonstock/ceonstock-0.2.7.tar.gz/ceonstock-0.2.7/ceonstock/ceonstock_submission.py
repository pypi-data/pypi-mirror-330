# Functions that help with the generation of project inputs.
import logging
from typing import List, Dict

from ceonstock import CstockJobInputType, CstockProjectInput
from ceonstock import CstockJobInput
from ceonstock import CstockSubmissionInput
from ceonstock import CstockWebInputType
from ceonstock.core.submission_input import CstockSubmissionInputEntry
from ceonstock.core.submission_input import CstockSubmissionInputRaw
from ceonstock.core.file_action import (
    CstockFileActionCrop,
    CstockFileActionDocToImgs,
)
from ceonstock.core.file_action import CstockFileAction
from ceonstock.core.file_action import CstockFileActionType
from ceonstock.log import printify

logger = logging.getLogger(__name__)

PREPROCESS_ACTIONS: Dict[CstockWebInputType, List[CstockFileAction]] = {
    CstockWebInputType.DOC: [
        CstockFileAction(
            CstockFileActionType.DOC_TO_IMGS, CstockFileActionDocToImgs()
        )
    ]
}


def create_submission_input_raw(
    cstock_project_input: CstockProjectInput,
    values: List,
) -> CstockSubmissionInputRaw:
    # TODO validate values are valid for this project input?
    # Get required actions for preprocessing this input.
    preprocess_actions = PREPROCESS_ACTIONS.get(
        cstock_project_input.web_input_type, []
    )
    submission_input_raw = CstockSubmissionInputRaw(
        values=values,
        project_input=cstock_project_input,
        preprocess_actions=preprocess_actions,
    )
    return submission_input_raw


def create_submission_input(
    cstock_project_input: CstockProjectInput,
    values: List,
) -> CstockSubmissionInput:
    """Receives a project input and the provided user entries.
    Returns a submission input."""
    entries = [
        CstockSubmissionInputEntry(value=value, entry_actions=[])
        for value in values
    ]
    return CstockSubmissionInput(
        project_input=cstock_project_input,
        entries=entries,
    )


# def create_submission(
#     project_inputs: List[CstockProjectInput], user_inputs_raw: List[CstockSubmissionInputRaw]
# ):
#     """Build the submission input instances from the received raw json from the web client."""
#     project_inputs_lookup = {
#         project_input.name: project_input for project_input in project_inputs
#     }

#     submission_inputs = []
#     for user_input_raw in user_inputs_raw:
#         entries = [SubmissionInputEntry(value=value, entry_actions=[]) for value in user_input_raw.values]
#         submission_input = CstockSubmissionInput(entries=entries, project_input=cstock_project_input)
#         submission_inputs.append(submission_input)
#     logger.info(f"Create submission inputs:{printify(submission_inputs)}")


def raw_to_submission_input(
    submission_input_raw: CstockSubmissionInputRaw,
) -> CstockSubmissionInput:
    """
    Convert raw input to submission input.
    Assumes that no pre-processing is required.
    In the case that pre-processign is required, it is the responsibility of the preprocessor
    to provide valid submission_inputs after preprocessing has completed.
    """
    if len(submission_input_raw.preprocess_actions) >= 1:
        # Don't allow this to be used if preprocessing is required
        raise Exception(
            f"Failed to convert raw submission inputs: "
            f"\t{submission_input_raw.project_input.name} contains preprocessing tasks: {submission_input_raw.preprocess_actions}"
            f"In this case it is the responsibility of the preprocessing server to generate correct submission inputs."
        )

    # Create an entry for each value
    entries = [
        CstockSubmissionInputEntry(value=value, entry_actions=[])
        for value in submission_input_raw.values
    ]
    return CstockSubmissionInput(
        entries=entries, project_input=submission_input_raw.project_input
    )


def raw_to_submission_inputs(
    user_inputs_raw: List[CstockSubmissionInputRaw],
) -> List[CstockSubmissionInput]:
    """
    Connvert a list of CstockSubmissionInputRaw to CstockSubmissionInput.
    """
    return [
        raw_to_submission_input(input_raw) for input_raw in user_inputs_raw
    ]


def submission_input_to_job_input(
    submission_input: CstockSubmissionInput,
) -> CstockJobInput:
    values = [entry.value for entry in submission_input.entries]
    return CstockJobInput(
        name=submission_input.project_input.name,
        job_input_type=submission_input.project_input.job_input_type,
        values=values,
    )


# TODO remove in favor of single conversion
# Currently kepts only for backwards compatibility.
def submission_inputs_to_job_inputs(
    submission_inputs: List[CstockSubmissionInput],
) -> List[CstockJobInput]:
    job_inputs = [
        submission_input_to_job_input(input) for input in submission_inputs
    ]
    return job_inputs


def validate_submission(
    project_inputs: List[CstockProjectInput],
    submission_inputs: List[CstockSubmissionInput],
):
    # TODO validate e.g. submission is missing required project inputs, or includes an unrecognized input..
    raise NotImplementedError
    pass


def submission_input_expects_files(
    submission_input: CstockSubmissionInput,
) -> bool:
    """Returns True if the submission receives files from the user.
    Returns False if no files are expected."""
    if (
        submission_input.project_input.web_input_type
        == CstockWebInputType.DROPDOWN
    ):
        # Although a dropdown web_input may produce a job_input that is a file (E.g. an img file), it does
        # not receive the file from the customer (In this case the image would be a fixed path in the project files)
        return False
    job_input_filetypes = [CstockJobInputType.IMG, CstockJobInputType.AUDIO]
    if submission_input.project_input.job_input_type in job_input_filetypes:
        return True
    return False
