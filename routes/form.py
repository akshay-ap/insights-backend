import json

from flask import Blueprint, request, jsonify
from methods.form import (
    save_submission,
    get_all_submissions_by_template,
    save_new_template,
    get_templates_by_id,
)

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
    return (
        json.dumps({"submission_id": submission_id}),
        200,
        {"ContentType": "application/json"},
    )


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
