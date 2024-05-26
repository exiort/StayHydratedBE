from flask import jsonify, request
from flask_jwt_extended import current_user
from sqlalchemy.exc import IntegrityError

from StayHydrated.models import db, User
from StayHydrated.utils.error import Error, ErrorType
from StayHydrated.utils.form_validator import validate_request_data
from StayHydrated.personal_data.controllers import create_personal_data


def create_user_controller(request_data: dict):
    try:
        new_user = User(
            name=request_data["name"],
            surname=request_data["surname"],
            email=request_data["email"],
            username=request_data["username"],
            password=request_data["password"],
        )

        db.session.add(new_user)
        db.session.commit()

        return "", 201

    except IntegrityError:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is already a User with same credentials!"
                ).serialize()
            ),
            422,
        )

    except Exception as e:
        return (
            jsonify(Error(ErrorType.DB_ERROR, "A Database error occured").serialize()),
            500,
        )


def delete_user_contoller():
    try:
        db.session.delete(current_user)
        db.session.commit()
        return "", 204

    except Exception as e:
        return (
            jsonify(Error(ErrorType.DB_ERROR, "A Database error occured").serialize()),
            500,
        )


def update_user_controller():
    required_fields = {
        "name": str,
        "surname": str,
        "email": str,
        "password": str,
    }
    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)

    try:
        current_user.name = request_data["name"]
        current_user.surname = request_data["surname"]
        current_user.email = request_data["email"]
        current_user.password = request_data["password"]

        db.session.commit()

        return "", 200

    except Exception as e:
        return (
            jsonify(Error(ErrorType.DB_ERROR, "A Database error occured").serialize()),
            500,
        )


def get_user_controller():
    return (
        jsonify(current_user.serialize()),
        200,
    )


def set_personal_data():
    if current_user.personal_data is not None:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is already a personal data"
                ).serialize()
            ),
            422,
        )

    required_fields = {
        "sex": bool,
        "born_date": str,
        "wake_up_time": str,
        "sleep_time": str,
        "weight": int,
        "height": int,
        "activity_level": int,
        "climate": int,
    }

    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)

    return create_personal_data(request_data)


def delete_personal_data():
    p_data = current_user.personal_data
    if p_data is None:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is no a personal data to delete"
                ).serialize()
            ),
            422,
        )
    try:
        db.session.delete(p_data)
        db.session.commit()
        return "", 204
    except Exception as e:
        return (
            jsonify(Error(ErrorType.DB_ERROR, "A Database error occured").serialize()),
            500,
        )


def update_personal_data():
    p_data = current_user.personal_data
    if p_data is None:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is no a personal data to update"
                ).serialize()
            ),
            422,
        )
    delete_personal_data()
    set_personal_data()
    return "", 200


def get_personal_data():
    p_data = current_user.personal_data
    if p_data is None:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is no a personal data to get"
                ).serialize()
            ),
            422,
        )

    return (
        jsonify(p_data.serialize()),
        200,
    )
