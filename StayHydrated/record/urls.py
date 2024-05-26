from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from StayHydrated.record.controllers import (
    create_record_controller,
    get_all_record_controller,
    get_bottle_record_controller,
    get_added_record_controller,
)

bp = Blueprint("record", __name__, url_prefix="/record")


@bp.route("", methods=["POST"])
@jwt_required()
def record():
    if request.method == "POST":
        return get_all_record_controller()


@bp.route("/create", methods=["POST"])
@jwt_required()
def create_record():
    if request.method == "POST":
        return create_record_controller()


@bp.route("/bottle", methods=["GET"])
@jwt_required()
def bottle():
    if request.method == "POST":
        return get_bottle_record_controller()


@bp.route("/added", methods=["GET"])
@jwt_required()
def added():
    if request.method == "GET":
        return get_added_record_controller()
