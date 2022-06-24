import logging

from eth_account.messages import encode_defunct
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from web3.auto import w3

from collection.user import User
from dao.UserManager import user_manager

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    public_address = data["public_address"]
    result, nonce = user_manager.register(public_address)
    if result:
        return jsonify({'nonce': nonce}), 200
    else:
        return jsonify({'errors': ["User already exists"]}), 400


@user_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    public_address = data["public_address"]
    signature = data.get["signature"]

    user: User = user_manager.get_by_public_address(public_address)
    access_token = create_access_token(identity=public_address,
                                       user_claims=user.get("roles"))
    refresh_token = create_refresh_token(identity=public_address,
                                         user_claims=user.get("roles"))

    message = encode_defunct(text=str(user.get("nonce")))
    try:
        signer = w3.eth.account.recover_message(message, signature=signature)
        if public_address == signer:
            return True
        else:
            logging.info(
                "Signature verification failed for [{}]. Signer not matched".format(
                    public_address
                )
            )
    except:
        logging.info(
            "Signature verification failed for [{}]".format(public_address)
        )
        return False
    return jsonify({
        'access-token': access_token,
        'refresh-token': refresh_token
    }), 200


@user_blueprint.route("/logout", methods=["POST"])
def logout():
    pass


@user_blueprint.route("/refresh", methods=["POST"])
def refresh():
    pass


@user_blueprint.route("/nonce", methods=["GET"])
def get_nonce():
    args = request.args
    public_address = args['public_address']
    nonce = user_manager.get_nonce(public_address)
    return jsonify({'nonce': nonce}), 200
