from marshmallow import Schema, fields, validate


class AuthSchema(Schema):
    firstname = fields.Str(
        required=True,
        error_messages={"required": "Firstname is required."},
        validate=validate.Length(min=2, max=32),
    )
    lastname = fields.Str(
        required=True,
        error_messages={"required": "Lastname is required."},
        validate=validate.Length(min=2, max=32),
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required."}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        error_messages={"required": "Password is required."}
    )


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required."}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6),
        error_messages={"required": "Password is required."}
    )
    is_active = fields.Boolean()
    is_admin = fields.Boolean()
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)
    sign_in_count = fields.Int(dump_only=True)
    current_sign_in_on = fields.DateTime(dump_only=True)
    last_sign_in_on = fields.DateTime(dump_only=True)
    current_sign_in_ip = fields.Str(
        dump_only=True,
        validate=validate.Length(max=32),
    )
    last_sign_in_ip = fields.Str(
        dump_only=True,
        validate=validate.Length(max=32),
    )
