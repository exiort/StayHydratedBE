from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from StayHydrated.user.controllers import (
    get_user_controller,
    delete_user_contoller,
    update_user_controller,
    set_personal_data,
    delete_personal_data,
    update_personal_data,
    get_personal_data,
)

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("", methods=["GET", "PATCH", "DELETE"])
@jwt_required()
def user():
    if request.method == "GET":
        return get_user_controller()
    elif request.method == "PATCH":
        return update_user_controller()
    elif request.method == "DELETE":
        return delete_user_contoller()


@bp.route("/profile", methods=["GET", "POST", "PATCH", "DELETE"])
@jwt_required()
def personal_data_settings():
    if request.method == "GET":
        return get_personal_data()
    elif request.method == "POST":
        return set_personal_data()
    elif request.method == "PATCH":
        return update_personal_data()
    elif request.method == "DELETE":
        return delete_personal_data()
