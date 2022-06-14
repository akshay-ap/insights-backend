import json

from flask import Blueprint, request, jsonify
from methods.form import (
    get_template_count,
    get_submission_count,
    get_user_count
)
from methods.stats import get_user_submission_count, get_user_submission_count_by_status, get_user_submission_list

stats_blueprint = Blueprint("stats_blueprint", __name__)


@stats_blueprint.route("/", methods=["GET"])
def get_stats():
    template_count = get_template_count()
    submission_count = get_submission_count()
    user_count = get_user_count()
    result = {
        "template_count": template_count,
        "submission_count": submission_count,
        "user_count": user_count
    }
    return jsonify(result), 200


@stats_blueprint.route("/user", methods=["GET"])
def get_user_stats():
    args = request.args
    public_address = args.get("public_address")

    submission_count = get_user_submission_count(public_address)
    (claimed, claimable, submitted) = get_user_submission_count_by_status(public_address)
    result = {
        "claimed-submissions": claimed,
        "total-submissions": submission_count,
        "submitted-submissions": submitted,
        "claimable-submissions": claimable
    }
    return jsonify(result), 200


@stats_blueprint.route('/user-submissions', methods=["GET"])
def get_user_submissions():
    args = request.args
    public_address = args.get("public_address")

    result = get_user_submission_list(public_address)
    return jsonify(result), 200
