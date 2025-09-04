from flask_smorest import Blueprint
from flask import request
from extension import db
from models import Meals, Children
from datetime import datetime

from schemas.meals import (
    Meal, CreateMeal, UpdateMeal,
)
from schemas.common import MessageSchema

blp = Blueprint("meals", __name__, url_prefix="/meals", description="meals CRUD API")

@blp.route("/", methods=["POST"])
@blp.arguments(CreateMeal()) # request schema
@blp.response(201, Meal()) # response schema
@blp.doc(description="Create a new meal record", tags=["meal"])
def create_meal(payload):
    # optional runtime check (not documented as error)
    if not Children.query.get(payload["child_id"]):
        return {"error": "Child not found"}, 404

    new_meal = Meals(
        meal_name=payload["meal_name"],
        servings_fruit=payload.get("servings_fruit", 0.0),
        servings_grain=payload.get("servings_grain", 0.0),
        servings_meat_fish_eggs_nuts_seeds=payload.get("servings_meat_fish_eggs_nuts_seeds", 0.0),
        servings_milk_yoghurt_cheese=payload.get("servings_milk_yoghurt_cheese", 0.0),
        servings_veg_legumes_beans=payload.get("servings_veg_legumes_beans", 0.0),
        child_id=payload["child_id"],
        meal_type=payload["meal_type"],
        created_at=datetime.now(),
    )
    db.session.add(new_meal)
    db.session.commit()
    return new_meal, 201


@blp.route("/child/<int:child_id>", methods=["GET"])
@blp.response(200, Meal(many=True)) # response schema (array of Meal)
@blp.doc(
    description="Get all meals for a specific child",
    tags=["meal"],
    parameters=[{
        "name": "child_id", "in": "path", "description": "ID of the child",
        "required": True, "schema": {"type": "integer"}
    }]
)
def get_meals_by_child(child_id):
    if not Children.query.get(child_id):
        return {"error": "Child not found"}, 404
    meals = Meals.query.filter_by(child_id=child_id).all()
    return meals


@blp.route("/<int:meal_id>", methods=["PUT"])
@blp.arguments(UpdateMeal()) # request schema (partial)
@blp.response(200, Meal()) # response schema
@blp.doc(
    description="Update a meal by ID",
    tags=["meal"],
    parameters=[{
        "name": "meal_id", "in": "path", "description": "ID of the meal",
        "required": True, "schema": {"type": "integer"}
    }]
)
def update_meal(payload, meal_id):
    meal = Meals.query.get_or_404(meal_id)
    for k, v in payload.items():
        setattr(meal, k, v)
    db.session.commit()
    return meal


@blp.route("/<int:meal_id>", methods=["DELETE"])
@blp.response(200, MessageSchema()) # response schema
@blp.doc(
    description="Delete a meal by ID",
    tags=["meal"],
    parameters=[{
        "name": "meal_id", "in": "path", "description": "ID of the meal",
        "required": True, "schema": {"type": "integer"}
    }]
)
def delete_meal(meal_id):
    meal = Meals.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return {"message": "Meal deleted"}