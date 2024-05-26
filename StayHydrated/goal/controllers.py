from flask import jsonify, request
from flask_jwt_extended import current_user

from StayHydrated.models import Goal
from StayHydrated.utils.error import Error, ErrorType
from StayHydrated.utils.form_validator import validate_request_data







def get_goal_controller():
    goal = current_user.goal
    if goal is None:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is no goal to get"
                ).serialize()
            ),
            422,
        )
    
    return (
        jsonify(goal.serialize()),
        200,
    )


def create_goal_controller():
    if current_user.goal is not None:
        return (
            jsonify(
                Error(
                    ErrorType.SEMANTIC, "There is already a goal"
                ).serialize()
            ),
            422,
        )

    required_fields = {
        
    }

    request_data = request.json

    is_valid, error = validate_request_data(request_data, required_fields)

    if not is_valid:
        return (jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400)
