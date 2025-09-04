from marshmallow import Schema, fields

class MessageSchema(Schema):
    message = fields.String(required=True)

class ErrorSchema(Schema):
    code = fields.Integer(load_default=None, allow_none=True)
    status = fields.String(load_default=None, allow_none=True)
    message = fields.String(required=True)
    errors = fields.Dict(keys=fields.String(), values=fields.Raw(), load_default=None, allow_none=True)