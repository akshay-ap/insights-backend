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


def mark_submission_claimable(submission_id):
    submission_db.submission.update_one(
        {"submission_id": submission_id, "type": DocumentType.submission},
        {
            "$set": {"status": SubmissionStatus.claimable}
        }
    )


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


def update_template(template_id: str, nft_address: str) -> None:
    form_db.templates.update_one(
        {"template_id": template_id},
        {
            "$set": {"nft_address": nft_address, "updated_at": datetime.datetime.utcnow()}
        }
    )


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


def get_nft_address(template_id: str) -> str:
    result = form_db.templates.find_one(
        {"template_id": template_id, "type": DocumentType.template}
    )
    return result.get("nft_address", None)


def update_user_submission_status(nft_address: str, public_address: str, transaction_hash: str, submission_id: str):
    form_db.submission.update_one(
        {"submission_id": submission_id, "public_address": public_address},
        {
            "$set": {"transaction_hash": transaction_hash, "updated_at": datetime.datetime.utcnow(),
                     "status": SubmissionStatus.claimed}
        }
    )


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


def get_reward(template_id: str) -> int:
    result = form_db.templates.find_one(
        {"template_id": template_id, "type": DocumentType.template}
    )
    template = result.get("template", None)
    return template.get("rewardPerSubmission", 0)
