from marshmallow import Schema, fields, validate

MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]

def _num():
    return fields.Float(validate=validate.Range(min=0), load_default=0.0)

# ----- Core entity -----
class _MealFields(Schema):
    meal_name = fields.String()
    servings_fruit = _num()
    servings_grain = _num()
    servings_meat_fish_eggs_nuts_seeds = _num()
    servings_milk_yoghurt_cheese = _num()
    servings_veg_legumes_beans = _num()
    child_id = fields.Int()
    meal_type = fields.String(validate=validate.OneOf(MEAL_TYPES))

# ----- Requests -----
class Meal(_MealFields):
    meal_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class CreateMeal(_MealFields):
    meal_name = fields.String(required=True)
    child_id = fields.Int(required=True)
    meal_type = fields.String(required=True, validate=validate.OneOf(MEAL_TYPES))

class UpdateMeal(_MealFields):
    pass

# Response envelopes
class MealMessageResponse(Schema):
    message = fields.String(required=True)
    meal = fields.Nested(Meal, required=True)
