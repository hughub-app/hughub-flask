from flask_smorest import Blueprint
from flask import request, jsonify
from .services import get_recommended_recipes
from models import DietaryGuidelines, Ingredient, Recipe

blp = Blueprint("recipes", __name__, url_prefix="/recipes",
                description="Recipe Recommander API")


@blp.route("/recommend", methods=["GET"])
def recommend_recipe():
    age = request.args.get("age", type=int)
    gender = request.args.get("gender", type=str)

    recipes = get_recommended_recipes(age, gender)
    return jsonify({"age": age, "gender": gender, "recipes": recipes})


# ---------------------------
# Read All APIs
# ---------------------------

@blp.route("/dietary-guidelines", methods=["GET"])
def get_all_dietary_guidelines():
    """Get all dietary_guidelines"""
    guidelines = DietaryGuidelines.query.all()
    result = [g.to_dict() for g in guidelines]
    return jsonify(result)


@blp.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    """Get all ingredients"""
    ingredients = Ingredient.query.all()
    result = [i.to_dict() for i in ingredients]
    return jsonify(result)


@blp.route("/", methods=["GET"])
def get_all_recipes():
    """Get all recipes"""
    recipes = Recipe.query.all()
    result = [r.to_dict() for r in recipes]
    return jsonify(result)
