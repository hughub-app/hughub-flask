from marshmallow import Schema, fields, validate

def _serv():
    return fields.Float(allow_none=True, validate=validate.Range(min=0))
    # return fields.Decimal(as_string=True, places=2, allow_none=True)

class _RecipeFields(Schema):
    recipe_name = fields.String()
    recipe_type = fields.String(allow_none=True)
    cuisine_type = fields.String(allow_none=True)
    dietary_preferences = fields.String(allow_none=True)
    cooking_steps = fields.String(allow_none=True)

    servings_veg_legumes_beans = _serv()
    servings_fruit = _serv()
    servings_grain = _serv()
    servings_meat_fish_eggs_nuts_seeds = _serv()
    servings_milk_yoghurt_cheese = _serv()

class Recipe(_RecipeFields):
    recipe_id = fields.Int(dump_only=True)

class CreateRecipe(_RecipeFields):
    recipe_name = fields.String(required=True, validate=validate.Length(min=1))

class UpdateRecipe(_RecipeFields):
    pass

class GetRecipesQuery(Schema):
    ids = fields.String(required=False, metadata={"description": "Comma-separated recipe IDs"})
    recipe_name = fields.String(required=False, metadata={"description": "ILIKE match"})
    recipe_type = fields.String(required=False)
    cuisine_type = fields.String(required=False)
    dietary_preferences = fields.String(required=False)