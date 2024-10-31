from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=30))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    full_name = fields.String(required=True, validate=validate.Length(min=3, max=100))