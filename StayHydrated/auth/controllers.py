from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
)
from werkzeug.security import check_password_hash


from StayHydrated.models import db, User
from StayHydrated.utils.form_validator import validate_request_data
from StayHydrated.utils.error import Error, ErrorType
from StayHydrated.user.controllers import create_user_controller

def auth_register_controller():
    required_fields = {
        "username":str,
        "password":str,
        "name":str,
        "surname":str,
        "email":str,
    }
    
    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)
    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)
    
    return create_user_controller(request_data)
    
def auth_login_controller():
    required_fields = {
        "username":str,
        "password":str,
    }

    request_data = request.json
    
    is_valid, error = validate_request_data(request_data, required_fields)
    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)
    

    user:User = db.session.scalars(
        db.select(User).where(User.username == request_data["username"])
    ).one_or_none()

    if user is None:
        return (
            jsonify(
                Error(
                    ErrorType.NOT_FOUND,
                    f"No such user with username -{request_data["username"]}-",
                ).serialize()
            ),
            404,
        )
    
    if not check_password_hash(user.password, request_data["password"]):
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC,
                    f"Wrong password entered"
                ).serialize()
            ),
            422,
        )
    
    access_token = create_access_token(
        identity=user.id
    )
    refresh_token = create_refresh_token(
        identity=user.id
    )

    return (
        jsonify(
            {
                "access_token":access_token,
                "refresh_token":refresh_token,
            }
        ),
        200,
    )

def refresh_token_controller():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)