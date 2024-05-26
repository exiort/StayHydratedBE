from flask_jwt_extended import current_user
from flask import jsonify

import datetime

from StayHydrated.models import db, PersonalData
from StayHydrated.utils.error import Error, ErrorType


def create_personal_data(request_data: dict):

    try:
        born_date = datetime.datetime.strptime(request_data["born_date"], "%d:%m:%Y")
        wake_up_time = datetime.datetime.strptime(request_data["wake_up_time"], "%H:%M")
        sleep_time = datetime.datetime.strptime(request_data["sleep_time"], "%H:%M")

    except:
        return (
            jsonify(Error(ErrorType.SYNTACTIC, "Check Time Syntax!").serialize()),
            400,
        )

    try:
        new_personal_data = PersonalData(
            current_user.id,
            1,
            request_data["sex"],
            born_date,
            wake_up_time,
            sleep_time,
            request_data["weight"],
            request_data["height"],
            request_data["activity_level"],
            request_data["climate"],
        )

        db.session.add(new_personal_data)
        db.session.commit()

        return "", 201
    except Exception as e:
        return (
            jsonify(Error(ErrorType.DB_ERROR, "A Database error occured").serialize()),
            500,
        )
