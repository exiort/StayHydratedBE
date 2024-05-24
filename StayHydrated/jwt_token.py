from flask_jwt_extended import JWTManager
from flask import jsonify

from StayHydrated.models import db, User

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]

    user: User = db.session.scalars(
        db.select(User).where(User.id == identity)
    ).one_or_none()

    return user


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed", "error": "invalid_token"}),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "message": "Request doesn't contain valid token",
                "error": "authorization_header",
            }
        ),
        403,
    )
