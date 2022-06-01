import datetime
import json
from enum import Enum
from typing import List

from bson import json_util

from db import submission_db, form_db
from utils.utils import get_random_string


class DocumentType(str, Enum):
    submission = "submission"
    template = "template"
    user = "user"


def save_submission(template_id: str, submission: object, public_address: str) -> str:
    submission_id = submission_db.submission.insert_one(
        {
            "type": DocumentType.submission,
            "submission": submission,
            "submission_id": generate_doc_id(DocumentType.submission),
            "public_address": public_address,
            "template_id": template_id,
            "created_at": datetime.datetime.utcnow(),
        }
    ).inserted_id

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
