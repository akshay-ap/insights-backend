import json

from flask import Blueprint, request, jsonify
from methods.form import (
    save_submission,
    get_all_submissions_by_template,
    save_new_template,
    get_templates_by_id, update_template, get_nft_address, mark_submission_claimable, update_user_submission_status,
)
from methods.nft_interaction import update_to_claimable

form_blueprint = Blueprint("form_blueprint", __name__)


@form_blueprint.route("/submit", methods=["POST"])
def save_form_submission():
    data = request.get_json()
    template_id = data["template-id"]
    submission = data["submission"]
    public_address = data["public_address"]

    submission_id = save_submission(
        template_id=template_id, submission=submission, public_address=public_address
    )

    nft_address = get_nft_address(template_id)
    if nft_address is not None:
        (success, hash) = update_to_claimable(nft_address, public_address)
        if success:
            mark_submission_claimable(submission_id)
    return (
        json.dumps({"submission_id": submission_id}),
        200,
        {"ContentType": "application/json"},
    )


@form_blueprint.route("/submission/update", methods=["POST"])
def update_user_submission():
    data = request.get_json()
    nft_address = data["nft_address"]
    public_address = data["account"]
    transaction_hash = data["transaction_hash"]
    submission_id = data["submission_id"]
    update_user_submission_status(
        nft_address=nft_address, public_address=public_address, transaction_hash=transaction_hash, submission_id=submission_id
    )

    return jsonify({}), 200


@form_blueprint.route("/template/update", methods=["POST"])
def update_template_with_nft_address():
    data = request.get_json()
    template_id = data["template-id"]
    nft_address = data["nft_address"]
    update_template(template_id=template_id, nft_address=nft_address)
    return jsonify({}), 200


@form_blueprint.route("/", methods=["GET"])
def get_all_submissions():
    args = request.args
    template_id = args.get("template-id")

    submissions = get_all_submissions_by_template(template_id=template_id)
    return {"submissions": submissions}, 200, {"ContentType": "application/json"}


@form_blueprint.route("/template/create", methods=["POST"])
def save_template():
    data = request.get_json()
    template = data["template"]
    public_address = data["public_address"]  # TODO
    template_id = save_new_template(public_address=public_address, template=template)
    return jsonify({"template_id": template_id}), 200


@form_blueprint.route("/template/", methods=["GET"])
def get_templates():
    args = request.args
    template_ids = args.getlist("template-id")

    result = get_templates_by_id(template_ids=template_ids)
    return jsonify(result), 200
