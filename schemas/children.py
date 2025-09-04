# schemas/children.py
from marshmallow import Schema, fields, validate

GENDERS = ["M", "F"]

# ----- Core entity -----
class _ChildFields(Schema):
    name = fields.String()
    date_of_birth = fields.Date()  # expects YYYY-MM-DD
    gender = fields.String(validate=validate.OneOf(GENDERS), allow_none=True)
    meals_per_day = fields.Integer(validate=validate.Range(min=1, max=10), allow_none=True)

class Child(_ChildFields):
    child_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# ----- Requests -----
class CreateChild(_ChildFields):
    name = fields.String(required=True)
    date_of_birth = fields.Date(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(GENDERS))
    meals_per_day = fields.Integer(required=True, validate=validate.Range(min=1, max=10))

class UpdateChild(_ChildFields):
    # All optional; partial patch-like update
    pass

# ----- Query Schemas -----
class GetChildrenQuery(Schema):
    # Accepts comma-separated IDs: ?ids=1,2,3
    ids = fields.String(
        required=False,
        metadata={"description": "Comma-separated child IDs (e.g., 1,2,3)"}
    )