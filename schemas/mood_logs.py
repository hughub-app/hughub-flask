from marshmallow import Schema, fields, validate

# Define allowed mood types
MOOD_TYPES = ["laugh", "happy", "neutral", "sad", "angry"]

# ----- Core entity -----
class MoodLog(Schema):
    mood_log_id = fields.Int(dump_only=True)
    child_id = fields.Int(required=True)
    mood = fields.String(required=True, validate=validate.Length(max=50))
    notes = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

# Query schemas
class MoodLogsRangeQuery(Schema):
    child_id = fields.Int(required=True)
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)

# ----- Requests -----
class CreateMoodLog(Schema):
    child_id = fields.Int(required=True)
    mood = fields.String(required=True, validate=validate.OneOf(MOOD_TYPES))
    notes = fields.String(allow_none=True)

class UpdateMoodLog(Schema):
    # Partial update: all optional
    mood = fields.String(validate=validate.OneOf(MOOD_TYPES))
    notes = fields.String(allow_none=True)

# ----- Responses -----
class MoodLogMessageResponse(Schema):
    message = fields.String(required=True)
    mood_log = fields.Nested(MoodLog, required=True)
