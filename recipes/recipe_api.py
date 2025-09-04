from flask_smorest import Blueprint
from flask import jsonify
from models import DietaryGuidelines, Ingredient, Recipe, RecipeIngredient
from schemas.dietary_guidelines import DietaryGuideline as DietaryGuidelineSchema, GetDietaryGuidelinesQuery
from schemas.ingredients import Ingredient as IngredientSchema, GetIngredientsQuery
from schemas.recipes import Recipe as RecipeSchema, GetRecipesQuery
from schemas.recipe_ingredients import RecipeIngredient as RecipeIngredientSchema, GetRecipeIngredientsQuery

blp = Blueprint("recipes", __name__, url_prefix="/recipes", description="Recipe Recommender API")

def _parse_ids(csv: str | None):
    if not csv:
        return []
    return [int(x) for x in csv.split(",") if x.strip().isdigit()]

# ---------------------------
# GET /recipes/dietary-guidelines
# ---------------------------
@blp.route("/dietary-guidelines", methods=["GET"])
@blp.arguments(GetDietaryGuidelinesQuery, location="query")
@blp.response(200, DietaryGuidelineSchema(many=True))
@blp.doc(description="Get dietary guidelines with optional filters.", tags=["recipes"])
def get_all_dietary_guidelines(q):
    ids = _parse_ids(q.get("ids"))
    gender = q.get("gender")
    age = q.get("age")

    query = DietaryGuidelines.query
    if ids:
        # NOTE: correct column name is guideline_id (not id)
        query = query.filter(DietaryGuidelines.guideline_id.in_(ids))
    if gender:
        query = query.filter(DietaryGuidelines.gender == gender)
    if age is not None:
        query = query.filter(DietaryGuidelines.min_age <= age,
                             DietaryGuidelines.max_age >= age)

    return query.all()

# ---------------------------
# GET /recipes/ingredients
# ---------------------------
@blp.route("/ingredients", methods=["GET"])
@blp.arguments(GetIngredientsQuery, location="query")
@blp.response(200, IngredientSchema(many=True))
@blp.doc(description="Get all ingredients with optional filters", tags=["recipes"])
def get_all_ingredients(q):
    ids = _parse_ids(q.get("ids"))
    category = q.get("category")
    ingredient_name = q.get("ingredient_name")

    query = Ingredient.query
    if ids:
        query = query.filter(Ingredient.ingredient_id.in_(ids))
    if category:
        query = query.filter(Ingredient.category == category)
    if ingredient_name:
        query = query.filter(Ingredient.ingredient_name.ilike(f"%{ingredient_name}%"))

    return query.all()

# ---------------------------
# GET /recipes/
# ---------------------------
@blp.route("/", methods=["GET"])
@blp.arguments(GetRecipesQuery, location="query")
@blp.response(200, RecipeSchema(many=True))
@blp.doc(description="Get recipes with optional filters.", tags=["recipes"])
def get_all_recipes(q):
    ids = _parse_ids(q.get("ids"))
    recipe_name = q.get("recipe_name")
    recipe_type = q.get("recipe_type")
    cuisine_type = q.get("cuisine_type")
    dietary_preferences = q.get("dietary_preferences")

    query = Recipe.query
    if ids:
        query = query.filter(Recipe.recipe_id.in_(ids))
    if recipe_name:
        query = query.filter(Recipe.recipe_name.ilike(f"%{recipe_name}%"))
    if recipe_type:
        query = query.filter(Recipe.recipe_type == recipe_type)
    if cuisine_type:
        query = query.filter(Recipe.cuisine_type == cuisine_type)
    if dietary_preferences:
        query = query.filter(Recipe.dietary_preferences == dietary_preferences)

    return query.all()

# ---------------------------
# GET /recipes/recipe_ingredients
# ---------------------------
@blp.route("/recipe_ingredients", methods=["GET"])
@blp.arguments(GetRecipeIngredientsQuery, location="query")
@blp.response(200, RecipeIngredientSchema(many=True))
@blp.doc(description="Get recipe ingredients with optional filters.", tags=["recipes"])
def get_recipe_ingredients(q):
    ids = _parse_ids(q.get("ids"))
    recipe_ids = _parse_ids(q.get("recipe_id"))
    ingredient_ids = _parse_ids(q.get("ingredient_id"))

    query = RecipeIngredient.query
    if ids:
        query = query.filter(RecipeIngredient.recipe_ingredient_id.in_(ids))
    if recipe_ids:
        query = query.filter(RecipeIngredient.recipe_id.in_(recipe_ids))
    if ingredient_ids:
        query = query.filter(RecipeIngredient.ingredient_id.in_(ingredient_ids))

    return query.all()