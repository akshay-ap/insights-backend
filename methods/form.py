import datetime
import json
from enum import Enum

from bson import json_util

from db import submission_db


class DocumentType(str, Enum):
    submission = 'submission'
    template = 'template'
    user = 'user'


def save_submission(template_id: str, submission: object, public_address: str) -> str:
    submission_id = submission_db.submission.insert_one({
        'type': DocumentType.submission,
        'submission': submission,
        'public_address': public_address,
        'template_id': template_id,
        'created_at': datetime.datetime.utcnow(),
    }).inserted_id

    return str(submission_id)


def get_all_submissions_by_template(template_id: str) -> [object]:
    cursor = submission_db.submission.find({
        'template_id': template_id,
        'type': DocumentType.submission
    })

    data = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])  # This does the trick!
        data.append(doc)

    # json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]

    return data
