import datetime
import json
from enum import Enum
from typing import List

from bson import json_util

from db import submission_db, form_db
from enums.form_enums import DocumentType, SubmissionStatus
from utils.utils import get_random_string


def save_submission(template_id: str, submission: object, public_address: str) -> str:
    submission_id = generate_doc_id(DocumentType.submission)
    submission_db.submission.insert_one(
        {
            "type": DocumentType.submission,
            "submission": submission,
            "submission_id": submission_id,
            "public_address": public_address,
            "template_id": template_id,
            "created_at": datetime.datetime.utcnow(),
            "status": SubmissionStatus.submitted
        }
    )

    return str(submission_id)


def get_all_submissions_by_template(template_id: str) -> [object]:
    cursor = submission_db.submission.find(
        {"template_id": template_id, "type": DocumentType.submission}
    )

    data = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # This does the trick!
        data.append(doc)

    # json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]

    return data


def save_new_template(public_address: str, template: object) -> str:
    template_id = generate_doc_id(DocumentType.template)

    form_db.templates.insert_one(
        {
            "type": DocumentType.template,
            "template": template,
            "template_id": template_id,
            "created_by": public_address,
            "created_at": datetime.datetime.utcnow(),
            "version": 1,
        }
    )

    return template_id


def get_templates_by_id(template_ids: List[str]) -> List[object]:
    cursor = form_db.templates.find(
        {"template_id": {"$in": template_ids}, "type": DocumentType.template},
        {"type": 0, "_id": 0},
    )
    data = []
    for doc in cursor:
        doc["created_at"] = doc["created_at"].isoformat()  # This does the trick!
        data.append(doc)
    return data


def generate_doc_id(document_type: DocumentType) -> str:
    return document_type + ":" + get_random_string(10)


def get_template_count() -> int:
    result = form_db.templates.count_documents({})
    return result


def get_submission_count() -> int:
    result = submission_db.submission.count_documents({})
    return result


def get_user_count() -> int:
    result = len(submission_db.submission.distinct('public_address'))
    return result
