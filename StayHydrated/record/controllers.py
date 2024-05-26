from flask import jsonify, request
from flask_jwt_extended import current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from datetime import datetime, timedelta

from StayHydrated.models import db, Record
from StayHydrated.utils.form_validator import validate_request_data
from StayHydrated.utils.error import Error, ErrorType


def create_record_controller():
    required_fields = {
        "amount": int,
        "record_type": bool,
    }
    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)

    try:
        new_record = Record(
            current_user.id,
            request_data["amount"],
            request_data["record_type"],
        )

        db.session.add(new_record)
        db.session.commit()

        return "", 200

    except Exception as e:
        print(e)
        return (
            jsonify(Error(ErrorType.DB_ERROR, "A Database error occured").serialize()),
            500,
        )


def get_all_record_controller():
    required_fields = {
        "date": str,
    }
    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)

    target_date = datetime.strptime(request_data["date"], "%Y-%m-%d").date()

    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date + timedelta(days=1), datetime.min.time())

    records = db.session.scalars(
        db.select(Record).where(
            and_(Record.time >= start_of_day, Record.time < end_of_day)
        )
    ).all()

    return (
        jsonify([record.serialize() for record in records]),
        200,
    )


def get_bottle_record_controller():
    required_fields = {
        "date": str,
    }
    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)

    target_date = datetime.strptime(request_data["date"], "%d-%m-%Y").date()

    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date + timedelta(days=1), datetime.min.time())

    records = db.session.scalars(
        db.select(Record).where(
            and_(
                Record.time >= start_of_day,
                Record.time < end_of_day,
                Record.type == True,
            )
        )
    ).all()

    return (
        jsonify([record.serialize() for record in records]),
        200,
    )


def get_added_record_controller():
    required_fields = {
        "date": str,
    }
    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)

    target_date = datetime.strptime(request_data["date"], "%d-%m-%Y").date()

    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date + timedelta(days=1), datetime.min.time())
    
    records = db.session.scalars(
        db.select(Record).where(
            and_(
                Record.time >= start_of_day,
                Record.time < end_of_day,
                Record.type == True,
            )
        )
    ).all()

    return (
        jsonify([record.serialize() for record in records]),
        200,
    )
