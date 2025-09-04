from marshmallow import Schema, fields, validate

GENDERS = ["M", "F"]  # adjust if needed

def _serv():
    return fields.Float(allow_none=True, validate=validate.Range(min=0))

class _DietaryGuidelineFields(Schema):
    gender = fields.String(validate=validate.OneOf(GENDERS))
    age_group = fields.String()
    servings_veg_legumes_beans = _serv()
    servings_fruit = _serv()
    servings_grain = _serv()
    servings_meat_fish_eggs_nuts_seeds = _serv()
    servings_milk_yoghurt_cheese = _serv()
    min_age = fields.Integer(validate=validate.Range(min=0))
    max_age = fields.Integer(validate=validate.Range(min=0))

class DietaryGuideline(_DietaryGuidelineFields):
    guideline_id = fields.Int(dump_only=True)

class CreateDietaryGuideline(_DietaryGuidelineFields):
    gender = fields.String(required=True, validate=validate.OneOf(GENDERS))
    age_group = fields.String(required=True)
    min_age = fields.Integer(required=True, validate=validate.Range(min=0))
    max_age = fields.Integer(required=True, validate=validate.Range(min=0))

class UpdateDietaryGuideline(_DietaryGuidelineFields):
    pass

class GetDietaryGuidelinesQuery(Schema):
    ids = fields.String(required=False, metadata={"description": "Comma-separated guideline IDs e.g. 1,2,3"})
    gender = fields.String(required=False, validate=validate.OneOf(GENDERS))
    age = fields.Integer(required=False, validate=validate.Range(min=0),
                         metadata={"description": "Matches min_age ≤ age ≤ max_age"})