import re
from marshmallow import Schema, fields, validate, validates, ValidationError


class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(
        validate=validate.Length(min=2, max=32),
        required=True,
        error_messages={"required": "Firstname is required."}
    )
    lastname = fields.Str(
        validate=validate.Length(min=2, max=32),
        required=True,
        error_messages={"required": "Lastname is required."}
    )
    username = fields.Str(validate=validate.Length(min=3, max=32))
    bio = fields.Str(validate=validate.Length(max=255))
    avatar = fields.Url(validate=validate.Length(max=255))
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)

    @validates('username')
    def validate_username(self, username):
        if re.match('^[a-zA-Z0-9_]+$', username) is None:
            raise ValidationError(
                'Username can only contain valid characters.'
            )

