from marshmallow import Schema, fields, validate

class _RecipeIngredientFields(Schema):
    recipe_id = fields.Int()
    ingredient_id = fields.Int()
    grams = fields.Int(allow_none=True, validate=validate.Range(min=0))

class RecipeIngredient(_RecipeIngredientFields):
    recipe_ingredient_id = fields.Int(dump_only=True)
    recipe_name = fields.String(dump_only=True, allow_none=True)
    ingredient_name = fields.String(dump_only=True, allow_none=True)

class CreateRecipeIngredient(_RecipeIngredientFields):
    recipe_id = fields.Int(required=True)
    ingredient_id = fields.Int(required=True)

class UpdateRecipeIngredient(_RecipeIngredientFields):
    pass

class GetRecipeIngredientsQuery(Schema):
    ids = fields.String(required=False, metadata={"description": "Comma-separated recipe_ingredient IDs"})
    recipe_id = fields.String(required=False, metadata={"description": "Comma-separated recipe IDs"})
    ingredient_id = fields.String(required=False, metadata={"description": "Comma-separated ingredient IDs"})