# children_info/children_api.py  (or similar path)
from flask_smorest import Blueprint
from flask import request
from extension import db
from models import Children  # assumes .to_dict() not needed; we return model, marshmallow dumps it
from datetime import datetime

from schemas.children import (
    Child, CreateChild, UpdateChild, GetChildrenQuery
)
from schemas.common import MessageSchema  # you already have this

blp = Blueprint("children", __name__, url_prefix="/children", description="Children CRUD API")

# ---------------------------
# Read All + filter by ids
# ---------------------------
@blp.route("/", methods=["GET"])
@blp.arguments(GetChildrenQuery, location="query")
@blp.response(200, Child(many=True))
@blp.doc(
    description="Get children with optional ID filter (comma-separated).",
    tags=["children"]
)
def get_children(query_args):
    raw_ids = query_args.get("ids")  # e.g. "1,2,3"
    ids = [int(x) for x in raw_ids.split(",")] if raw_ids else []

    q = Children.query
    if ids:
        q = q.filter(Children.child_id.in_(ids))

    children = q.all()
    return children  # marshmallow handles serialization


# ---------------------------
# Create
# ---------------------------
@blp.route("/", methods=["POST"])
@blp.arguments(CreateChild)               # request schema
@blp.response(201, Child)                 # response schema
@blp.doc(description="Create a new child", tags=["children"])
def create_child(payload):
    child = Children(
        name=payload["name"],
        gender=payload["gender"],
        date_of_birth=payload["date_of_birth"],  # marshmallow parsed into date
        meals_per_day=payload["meals_per_day"],
        # created_at=datetime.utcnow(),  # only if your model doesn't auto-set
    )
    db.session.add(child)
    db.session.commit()
    return child, 201


# ---------------------------
# Update
# ---------------------------
@blp.route("/<int:child_id>", methods=["PUT"])
@blp.arguments(UpdateChild)               # partial update allowed by schema
@blp.response(200, Child)
@blp.doc(
    description="Update a child by ID",
    tags=["children"],
    parameters=[{
        "name": "child_id", "in": "path", "required": True,
        "schema": {"type": "integer"}, "description": "Child ID to update"
    }]
)
def update_child(payload, child_id):
    child = Children.query.get_or_404(child_id)

    # Apply only provided fields
    for k, v in payload.items():
        setattr(child, k, v)

    db.session.commit()
    return child


# ---------------------------
# Delete
# ---------------------------
@blp.route("/<int:child_id>", methods=["DELETE"])
@blp.response(200, MessageSchema())
@blp.doc(
    description="Delete a child by ID",
    tags=["children"],
    parameters=[{
        "name": "child_id", "in": "path", "required": True,
        "schema": {"type": "integer"}, "description": "Child ID to delete"
    }]
)
def delete_child(child_id):
    child = Children.query.get_or_404(child_id)
    db.session.delete(child)
    db.session.commit()
    return {"message": f"Child {child_id} deleted successfully"}