from flask import request, jsonify
from flask_smorest import Blueprint
from extension import db
from models import Child
from datetime import datetime

blp = Blueprint("children", __name__, url_prefix="/children",
                description="Children Info Management API")

@blp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# Create
@blp.route("/", methods=["POST"])
def create_child():
    data = request.get_json()
    child = Child(
        name=data["name"],
        dateOfBirth=datetime.strptime(data["dateOfBirth"], "%Y-%m-%d").date(),
        gender=data["gender"],
        heightCm=data.get("heightCm"),
        weightKg=data.get("weightKg")
    )
    db.session.add(child)
    db.session.commit()
    return jsonify({"message": "Child created", "child": child.to_dict()}), 201

# Read all
@blp.route("/", methods=["GET"])
def get_children():
    children = Child.query.all()
    return jsonify([c.to_dict() for c in children])

# Read one
@blp.route("/<int:child_id>", methods=["GET"])
def get_child(child_id):
    child = Child.query.get_or_404(child_id)
    return jsonify(child.to_dict())

# Update
@blp.route("/<int:child_id>", methods=["PUT"])
def update_child(child_id):
    data = request.get_json()
    child = Child.query.get_or_404(child_id)

    child.name = data.get("name", child.name)
    if "dateOfBirth" in data:
        child.dateOfBirth = datetime.strptime(data["dateOfBirth"], "%Y-%m-%d").date()
    child.gender = data.get("gender", child.gender)
    child.heightCm = data.get("heightCm", child.heightCm)
    child.weightKg = data.get("weightKg", child.weightKg)

    db.session.commit()
    return jsonify({"message": "Child updated", "child": child.to_dict()})

# Delete
@blp.route("/<int:child_id>", methods=["DELETE"])
def delete_child(child_id):
    child = Child.query.get_or_404(child_id)
    db.session.delete(child)
    db.session.commit()
    return jsonify({"message": "Child deleted"})
