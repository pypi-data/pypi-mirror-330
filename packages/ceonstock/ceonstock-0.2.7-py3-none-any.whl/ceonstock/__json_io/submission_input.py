from typing import Dict
from ceonstock import CstockSubmissionInput
from ceonstock.core.submission_input import SubmissionInputEntry


def serialize_entry(submission_input_entry: SubmissionInputEntry) -> Dict:
    as_dict = submission_input_entry.__dict__
    return as_dict


def serialize(cstock_submission_input: CstockSubmissionInput) -> Dict:
    entries_serialized = [
        serialize_entry(entry) for entry in cstock_submission_input.entries
    ]
    as_dict = CstockSubmissionInput.__dict__
    as_dict["entries"] = entries_serialized
    return as_dict
