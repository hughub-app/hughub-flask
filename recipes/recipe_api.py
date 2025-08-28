from flask_smorest import Blueprint
from flask import request, jsonify
from .services import get_recommended_recipes

blp = Blueprint("recipes", __name__, url_prefix="/recipes",
                description="Recipe Recommander API")

@blp.route("/recommend", methods=["GET"])
def recommend_recipe():
    age = request.args.get("age", type=int)
    gender = request.args.get("gender", type=str)

    recipes = get_recommended_recipes(age, gender)
    return jsonify({"age": age, "gender": gender, "recipes": recipes})
