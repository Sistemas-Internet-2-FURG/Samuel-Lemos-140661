from marshmallow import Schema, fields, validates_schema, ValidationError, validate

class UserSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class CourseSchema(Schema):
    name = fields.Str(required=True)
