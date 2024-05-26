import os
from flask import Flask
from flask_migrate import Migrate
from datetime import timedelta
from werkzeug.exceptions import NotFound, MethodNotAllowed

from StayHydrated.models import *
from StayHydrated.jwt_token import jwt
from StayHydrated.utils.error import handle_404_error, handle_405_error

from StayHydrated.auth.urls import bp as auth_bp
from StayHydrated.user.urls import bp as user_bp
from StayHydrated.record.urls import bp as record_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        JWT_SECRET_KEY="super-secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///stayhydrated.db",
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
    )
    
    os.makedirs(app.instance_path, exist_ok = True)

    migrate = Migrate(app, db)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(record_bp)

    app.register_error_handler(MethodNotAllowed, handle_405_error)
    app.register_error_handler(NotFound, handle_404_error)

    return app