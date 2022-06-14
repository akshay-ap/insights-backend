from enum import Enum


class SubmissionStatus(str, Enum):
    claimed = "claimed"
    claimable = "claimable"
    submitted = "submitted"


class DocumentType(str, Enum):
    submission = "submission"
    template = "template"
    user = "user"
