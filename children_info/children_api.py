from flask_smorest import Blueprint
from flask import request, jsonify
from extension import db
from models import Children
from datetime import datetime

blp = Blueprint("children", __name__, url_prefix="/children",
                description="Children CRUD API")


@blp.route("/", methods=["GET"])
@blp.doc(
    parameters=[
        {
            "in": "query",
            "name": "ids",
            "schema": {"type": "string"},
            "required": False,
            "description": "Filter by child IDs (comma separated, e.g. ids=1,2,3)"
        }
    ],
    responses={
        200: {
            "description": "List of children",
            "content": {
                "application/json": {
                    "example": [
                        {"child_id": 1, "name": "Tom", "gender": "Male", "date_of_birth": "2018-06-12"}
                    ]
                }
            }
        }
    }
)
def get_children():
    raw_ids = request.args.get("ids")  # e.g. ?ids=1,2,3
    ids = [int(x) for x in raw_ids.split(",")] if raw_ids else []

    query = Children.query
    if ids:
        query = query.filter(Children.child_id.in_(ids))

    children = query.all()
    return jsonify([c.to_dict() for c in children])


@blp.route("/", methods=["POST"])
@blp.doc(
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "name": "Alice",
                    "gender": "F",
                    "date_of_birth": "2019-05-20",
                    "meals_per_day": 3
                }
            }
        }
    },
    responses={
        201: {
            "description": "Child created",
            "content": {
                "application/json": {
                    "example": {"child_id": 2, "name": "Alice", "gender": "Female", "date_of_birth": "2019-05-20"}
                }
            }
        }
    }
)
def create_child():
    data = request.get_json()
    name = data.get("name")
    gender = data.get("gender")
    dob_str = data.get("date_of_birth")
    meals_per_day = data.get("meals_per_day")

    if not (name and gender and dob_str and meals_per_day is not None):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    child = Children(name=name, gender=gender, date_of_birth=date_of_birth, meals_per_day=meals_per_day)
    db.session.add(child)
    db.session.commit()

    return jsonify(child.to_dict()), 201


@blp.route("/<int:child_id>", methods=["PUT"])
@blp.doc(
    parameters=[
        {
            "in": "path",
            "name": "child_id",
            "schema": {"type": "integer"},
            "required": True,
            "description": "Child ID to update"
        }
    ],
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "name": "Alice Updated",
                    "gender": "F",
                    "date_of_birth": "2019-05-20"
                }
            }
        }
    },
    responses={
        200: {
            "description": "Child updated",
            "content": {
                "application/json": {
                    "example": {"child_id": 2, "name": "Alice Updated", "gender": "Female", "date_of_birth": "2019-05-20"}
                }
            }
        }
    }
)
def update_child(child_id):
    child = Children.query.get_or_404(child_id)
    data = request.get_json()

    if "name" in data:
        child.name = data["name"]
    if "gender" in data:
        child.gender = data["gender"]
    if "date_of_birth" in data:
        try:
            child.date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400
    if "meals_per_day" in data:
        child.meals_per_day = data["meals_per_day"]

    db.session.commit()
    return jsonify(child.to_dict())


@blp.route("/<int:child_id>", methods=["DELETE"])
@blp.doc(
    parameters=[
        {
            "in": "path",
            "name": "child_id",
            "schema": {"type": "integer"},
            "required": True,
            "description": "Child ID to delete"
        }
    ],
    responses={
        200: {
            "description": "Child deleted",
            "content": {
                "application/json": {
                    "example": {"message": "Child 2 deleted successfully"}
                }
            }
        }
    }
)
def delete_child(child_id):
    child = Children.query.get_or_404(child_id)
    db.session.delete(child)
    db.session.commit()
    return jsonify({"message": f"Child {child_id} deleted successfully"})

