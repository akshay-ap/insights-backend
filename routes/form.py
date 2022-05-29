import json

from flask import Blueprint, request
from methods.form import save_submission, get_all_submissions_by_template

form_blueprint = Blueprint("form_blueprint", __name__)


@form_blueprint.route('/submit', methods=["POST"])
def save_from_submission():
    data = request.get_json()
    template_id = data["template-id"]
    submission = data["submission"]
    public_address = ''  # TODO
    submission_id = save_submission(template_id=template_id, submission=submission, public_address=public_address)
    return json.dumps({'submission_id': submission_id}), 200, {'ContentType': 'application/json'}


@form_blueprint.route('/', methods=["GET"])
def get_all_submissions():
    args = request.args
    template_id = args.get('template-id')

    submissions = get_all_submissions_by_template(template_id=template_id)
    return {'submissions': submissions}, 200, {'ContentType': 'application/json'}
