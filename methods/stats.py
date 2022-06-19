from typing import List

from db import submission_db
from enums.form_enums import SubmissionStatus


def get_user_submission_count(public_address: str) -> int:
    result = submission_db.submission.count_documents({"public_address": public_address})
    return result


def get_user_submission_count_by_status(public_address: str) -> tuple:
    db_result = submission_db.submission.aggregate([
        {
            '$match': {
                'public_address': public_address
            }
        }, {
            '$group': {
                '_id': '$status',
                'count': {
                    '$sum': 1
                }
            }
        }
    ])

    # result = submission_db.submission.find({"public_address": public_address})
    # result_count = result.count(True)
    data = {}
    for status in SubmissionStatus:
        data[status] = 0

    for r in db_result:
        data[r["_id"]] = r["count"]

    return data[SubmissionStatus.claimed], data[SubmissionStatus.claimable], data[SubmissionStatus.submitted]


def get_user_submission_list(public_address: str) -> List[object]:
    db_result = submission_db.submission.aggregate([
        {
            '$match': {
                'public_address': public_address
            }
        }, {
            '$lookup': {
                'from': 'templates',
                'localField': 'template_id',
                'foreignField': 'template_id',
                'as': 'template'
            }
        }, {
            '$project': {
                'created_at': 1,
                '_id': 0,
                'status': 1,
                'reward': 1,
                'template_id': 1,
                'template': 1,
                'submission_id': 1,
                'transaction_hash': 1
            }
        }, {
            '$sort': {
                'created_at': -1
            }
        }
    ])

    data = []
    for r in db_result:
        data.append({
            'created_at': r['created_at'],
            'nft_address': r['template'][0]['nft_address'],
            'reward': r['template'][0].get('reward'),
            'name': r['template'][0]['template']['name'],
            'status': r['status'],
            'reward-token-address': r['template'][0]['template']['erc20TokenAddress'],
            'id': r['submission_id'],
            'transaction_hash': r.get('transaction_hash')
        })

    return data
