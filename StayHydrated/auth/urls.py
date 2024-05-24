from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from StayHydrated.models import db, User
from StayHydrated.utils.error import Error, ErrorType
from StayHydrated.utils.form_validator import validate_request_data

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

        return (
            jsonify(
                {
                    "user": {
                        **new_user.serialize()
                    }
                }
            ),
            201,
        )


    except IntegrityError:
        pass

    except Exception:
        pass