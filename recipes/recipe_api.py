from flask_smorest import Blueprint
from flask import request, jsonify
from .services import get_recommended_recipes
from models import DietaryGuidelines, Ingredient, Recipe, RecipeIngredient

blp = Blueprint("recipes", __name__, url_prefix="/recipes",
                description="Recipe Recommander API")


# ---------------------------
# Read All APIs
# ---------------------------

@blp.route("/dietary-guidelines", methods=["GET"])
@blp.doc(
    description="Get dietary guidelines with optional filters.",
    parameters=[
        {
            "name": "ids",
            "in": "query",
            "description": "Comma-separated list of guideline IDs, e.g., 1,2,3",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "gender",
            "in": "query",
            "description": "Filter by gender",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "age",
            "in": "query",
            "description": "Filter by age range (min_age ≤ age ≤ max_age)",
            "required": False,
            "schema": {"type": "integer"}
        }
    ]
)
def get_all_dietary_guidelines():
    """
    Get dietary guidelines with filters
    ---
    parameters:
      - in: query
        name: ids
        schema:
          type: array
          items:
            type: integer
        required: false
        description: Filter by guideline IDs
      - in: query
        name: gender
        schema:
          type: string
        required: false
        description: Filter by gender
      - in: query
        name: age
        schema:
          type: integer
        required: false
        description: Filter by age range (min_age ≤ age ≤ max_age)
    responses:
      200:
        description: List of guidelines
    """
    ids = request.args.getlist("ids", type=int)
    gender = request.args.get("gender")
    age = request.args.get("age", type=int)
    
    query = DietaryGuidelines.query
    if ids:
        query = query.filter(DietaryGuidelines.id.in_(ids))
    if gender:
        query = query.filter(DietaryGuidelines.gender == gender)
    if age is not None:
        query = query.filter(
            DietaryGuidelines.min_age <= age,
            DietaryGuidelines.max_age >= age
        )

    guidelines = query.all()
    result = [g.to_dict() for g in guidelines]
    return jsonify(result)


@blp.route("/ingredients", methods=["GET"])
@blp.doc(parameters=[
    {"name": "ids", "in": "query", "type": "array", "collectionFormat": "multi", "description": "Ingredient IDs to filter, e.g. ids=1,2,5"},
    {"name": "category", "in": "query", "type": "string", "description": "Category name to filter"},
    {"name": "ingredient_name", "in": "query", "type": "string", "description": "Ingredient name (partial match) to filter"},
])
def get_all_ingredients():
    """Get all ingredients with optional filters"""
    raw_ids = request.args.get("ids")  # "1,2"
    ids = [int(x) for x in raw_ids.split(",")] if raw_ids else []   
    category = request.args.get("category", type=str)
    ingredient_name = request.args.get("ingredient_name", type=str)


    query = Ingredient.query

    # apply filters
    if ids:
        query = query.filter(Ingredient.ingredient_id.in_(ids))
    if category:
        query = query.filter(Ingredient.category == category)
    if ingredient_name:
        query = query.filter(Ingredient.ingredient_name.ilike(f"%{ingredient_name}%"))

    ingredients = query.all()

    result = [i.to_dict() for i in ingredients]
    return jsonify(result)



@blp.route("/", methods=["GET"])
@blp.doc(
    description="Get recipes with optional filters.",
    parameters=[
        {
            "name": "ids",
            "in": "query",
            "description": "Comma-separated list of recipe IDs, e.g., 1,2,3",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "recipe_name",
            "in": "query",
            "description": "Filter recipes whose name ILIKE this string",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "recipe_type",
            "in": "query",
            "description": "Filter by recipe type",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "cuisine_type",
            "in": "query",
            "description": "Filter by cuisine type",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "dietary_preferences",
            "in": "query",
            "description": "Filter by dietary preferences",
            "required": False,
            "schema": {"type": "string"}
        },
    ]
)
def get_all_recipes():
    """Get recipes with optional filters"""
    raw_ids = request.args.get("ids")  # "1,2,3"
    ids_list = [int(x) for x in raw_ids.split(",")] if raw_ids else []

    recipe_name = request.args.get("recipe_name", type=str)
    recipe_type = request.args.get("recipe_type", type=str)
    cuisine_type = request.args.get("cuisine_type", type=str)
    dietary_preferences = request.args.get("dietary_preferences", type=str)

    query = Recipe.query

    # apply filters
    if ids_list:
        query = query.filter(Recipe.recipe_id.in_(ids_list))
    if recipe_name:
        query = query.filter(Recipe.recipe_name.ilike(f"%{recipe_name}%"))
    if recipe_type:
        query = query.filter(Recipe.recipe_type == recipe_type)
    if cuisine_type:
        query = query.filter(Recipe.cuisine_type == cuisine_type)
    if dietary_preferences:
        query = query.filter(Recipe.dietary_preferences == dietary_preferences)

    recipes = query.all()
    result = [r.to_dict() for r in recipes]
    return jsonify(result)


@blp.route("/recipe_ingredients", methods=["GET"])
@blp.doc(
    description="Get recipe ingredients with optional filters.",
    parameters=[
        {
            "name": "ids",
            "in": "query",
            "description": "Comma-separated list of recipe_ingredient IDs, e.g., 1,2,3",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "recipe_id",
            "in": "query",
            "description": "Comma-separated list of recipe IDs to filter",
            "required": False,
            "schema": {"type": "string"}
        },
        {
            "name": "ingredient_id",
            "in": "query",
            "description": "Comma-separated list of ingredient IDs to filter",
            "required": False,
            "schema": {"type": "string"}
        }
    ]
)
def get_recipe_ingredients():
    """Get recipe ingredients with optional filters"""
    # Parse comma-separated lists
    raw_ids = request.args.get("ids")
    ids = [int(x) for x in raw_ids.split(",")] if raw_ids else []

    raw_recipe_ids = request.args.get("recipe_id")
    recipe_ids = [int(x) for x in raw_recipe_ids.split(",")] if raw_recipe_ids else []

    raw_ingredient_ids = request.args.get("ingredient_id")
    ingredient_ids = [int(x) for x in raw_ingredient_ids.split(",")] if raw_ingredient_ids else []

    query = RecipeIngredient.query
    if ids:
        query = query.filter(RecipeIngredient.recipe_ingredient_id.in_(ids))
    if recipe_ids:
        query = query.filter(RecipeIngredient.recipe_id.in_(recipe_ids))
    if ingredient_ids:
        query = query.filter(RecipeIngredient.ingredient_id.in_(ingredient_ids))

    ingredients = query.all()
    result = [ri.to_dict() for ri in ingredients]  # Need to define to_dict in RecipeIngredient model
    return jsonify(result)