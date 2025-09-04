from marshmallow import Schema, fields, validate

class _IngredientFields(Schema):
    ingredient_name = fields.String()
    category = fields.String()
    emoji = fields.String(allow_none=True)

class Ingredient(_IngredientFields):
    ingredient_id = fields.Int(dump_only=True)

class CreateIngredient(_IngredientFields):
    ingredient_name = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(required=True)

class UpdateIngredient(_IngredientFields):
    pass

class GetIngredientsQuery(Schema):
    ids = fields.String(required=False, metadata={"description": "Comma-separated ingredient IDs"})
    category = fields.String(required=False)
    ingredient_name = fields.String(required=False, metadata={"description": "Partial match"})