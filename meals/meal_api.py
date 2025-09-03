from flask_smorest import Blueprint
from flask import request, jsonify
from extension import db
from models import Meals, Children
from datetime import datetime

blp = Blueprint("meals", __name__, url_prefix="/meals",
                description="meals CRUD API")


@blp.route("/", methods=["POST"])
@blp.doc(
    description="Create a new meal record",
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "meal_name": {"type": "string"},
                        "servings_fruit": {"type": "number"},
                        "servings_grain": {"type": "number"},
                        "servings_meat_fish_eggs_nuts_seeds": {"type": "number"},
                        "servings_milk_yoghurt_cheese": {"type": "number"},
                        "servings_veg_legumes_beans": {"type": "number"},
                        "child_id": {"type": "integer"},
                        "meal_type": {"type": "string"}
                    },
                    "required": ["meal_name", "child_id", "meal_type"]
                }
            }
        }
    },
    responses={201: {"description": "Meal created successfully"}}
)
def create_meal():
    """
    Create a new meal
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              meal_name:
                type: string
              servings_fruit:
                type: number
              servings_grain:
                type: number
              servings_meat_fish_eggs_nuts_seeds:
                type: number
              servings_milk_yoghurt_cheese:
                type: number
              servings_veg_legumes_beans:
                type: number
              child_id:
                type: integer
              meal_type:
                type: string
    responses:
      201:
        description: Meal created successfully
    """
    data = request.get_json()
    servings_fruit = data.get("servings_fruit", 0)
    servings_grain = data.get("servings_grain", 0)
    

    new_meal = Meals(
        meal_name=data["meal_name"],
        servings_fruit=data.get("servings_fruit"),
        servings_grain=data.get("servings_grain"),
        servings_meat_fish_eggs_nuts_seeds=data.get("servings_meat_fish_eggs_nuts_seeds", 0),
        servings_milk_yoghurt_cheese=data.get("servings_milk_yoghurt_cheese", 0),
        servings_veg_legumes_beans=data.get("servings_veg_legumes_beans", 0),
        child_id=data["child_id"],
        meal_type=data["meal_type"],
        created_at=datetime.now()
    )

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message": "Meal created", "meal": new_meal.to_dict()}), 201


@blp.route("/child/<int:child_id>", methods=["GET"])
@blp.doc(
    description="Get all meals for a specific child",
    parameters=[
        {
            "name": "child_id",
            "in": "path",
            "description": "ID of the child",
            "required": True,
            "schema": {"type": "integer"}
        }
    ],
    responses={
        200: {"description": "List of meals for the child"},
        404: {"description": "Child not found"}
    }
)
def get_meals_by_child(child_id):
    """
    Get all meals for a child
    ---
    parameters:
      - in: path
        name: child_id
        schema:
          type: integer
        required: true
        description: ID of the child
    responses:
      200:
        description: List of meals for the child
      404:
        description: Child not found
    """
    if not Children.query.get(child_id):
        return jsonify({"error": "Child not found"}), 404
    query = Meals.query
    query = query.filter_by(child_id=child_id)
    meals = query.all()
    # meals = Meals.query.filter_by(child_id=child_id).all()
    return jsonify([m.to_dict() for m in meals])



@blp.route("/<int:meal_id>", methods=["PUT"])
@blp.doc(
    description="Update a meal by ID",
    parameters=[
        {
            "name": "meal_id",
            "in": "path",
            "description": "ID of the meal",
            "required": True,
            "schema": {"type": "integer"}
        }
    ],
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "meal_name": {"type": "string"},
                        "servings_fruit": {"type": "number"},
                        "servings_grain": {"type": "number"},
                        "servings_meat_fish_eggs_nuts_seeds": {"type": "number"},
                        "servings_milk_yoghurt_cheese": {"type": "number"},
                        "servings_veg_legumes_beans": {"type": "number"},
                        "meal_type": {"type": "string"}
                    }
                }
            }
        }
    },
    responses={
        200: {"description": "Meal updated successfully"},
        404: {"description": "Meal not found"}
    }
)
def update_meal(meal_id):
    """
    Update a meal
    ---
    parameters:
      - in: path
        name: meal_id
        schema:
          type: integer
        required: true
        description: ID of the meal
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              meal_name:
                type: string
              servings_fruit:
                type: number
              servings_grain:
                type: number
              servings_meat_fish_eggs_nuts_seeds:
                type: number
              servings_milk_yoghurt_cheese:
                type: number
              servings_veg_legumes_beans:
                type: number
              meal_type:
                type: string
    responses:
      200:
        description: Meal updated successfully
      404:
        description: Meal not found
    """
    data = request.get_json()
    meal = Meals.query.get_or_404(meal_id)

    meal.meal_name = data.get("meal_name", meal.meal_name)
    meal.servings_fruit = data.get("servings_fruit", meal.servings_fruit)
    meal.servings_grain = data.get("servings_grain", meal.servings_grain)
    meal.servings_meat_fish_eggs_nuts_seeds = data.get("servings_meat_fish_eggs_nuts_seeds", meal.servings_meat_fish_eggs_nuts_seeds)
    meal.servings_milk_yoghurt_cheese = data.get("servings_milk_yoghurt_cheese", meal.servings_milk_yoghurt_cheese)
    meal.servings_veg_legumes_beans = data.get("servings_veg_legumes_beans", meal.servings_veg_legumes_beans)
    meal.meal_type = data.get("meal_type", meal.meal_type)

    db.session.commit()

    return jsonify({"message": "Meal updated", "meal": meal.to_dict()})


@blp.route("/<int:meal_id>", methods=["DELETE"])
@blp.doc(
    description="Delete a meal by ID",
    parameters=[
        {
            "name": "meal_id",
            "in": "path",
            "description": "ID of the meal",
            "required": True,
            "schema": {"type": "integer"}
        }
    ],
    responses={
        200: {"description": "Meal deleted successfully"},
        404: {"description": "Meal not found"}
    }
)
def delete_meal(meal_id):
    """
    Delete a meal
    ---
    parameters:
      - in: path
        name: meal_id
        schema:
          type: integer
        required: true
        description: ID of the meal
    responses:
      200:
        description: Meal deleted successfully
      404:
        description: Meal not found
    """
    meal = Meals.query.get_or_404(meal_id)

    db.session.delete(meal)
    db.session.commit()

    return jsonify({"message": "Meal deleted"})