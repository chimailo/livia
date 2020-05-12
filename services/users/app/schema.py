import re
from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, error_messages={
        "required": "Email is required."})
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6),
        error_messages={"required": "Password is required."}
    )
    firstname = fields.Str(validate=validate.Length(min=3, max=128))
    lastname = fields.Str(validate=validate.Length(min=3, max=128))
    username = fields.Str(validate=validate.Length(min=3, max=32))
    bio = fields.Str(validate=validate.Length(max=255))
    is_active = fields.Boolean()
    is_admin = fields.Boolean()
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)
    sign_in_count = fields.Int(dump_only=True)
    current_sign_in_on = fields.DateTime(dump_only=True)
    last_sign_in_on = fields.DateTime(dump_only=True)
    current_sign_in_ip = fields.Str(
        dump_only=True,
        validate=validate.Length(min=3, max=32),
    )
    last_sign_in_ip = fields.Str(
        dump_only=True,
        validate=validate.Length(min=3, max=32),
    )
    # groups = fields.List(
    #     fields.Nested(
    #         "GroupSchema", only=('name',), dump_only=True
    #     )
    # )

    @validates('username')
    def validate_username(self, username):
        if re.match('^[a-zA-Z0-9_]+$', username) is None:
            raise ValidationError(
                'Username can only contain valid characters.'
            )


# class GroupSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(
#         required=True,
#         error_messages={
#             "required": "A group must have a name."
#         },
#         validate=validate.Length(min=3, max=64),
#     )
#     description = fields.Str()
#     created_on = fields.DateTime(dump_only=True)
#     updated_on = fields.DateTime(dump_only=True)
#     users = fields.List(
#         fields.Nested(
#             "UserSchema", only=('id', 'email'), dump_only=True
#         )
#     )
    # permissions = fields.List(
    #     fields.Nested(
    #         lambda: PermissionSchema(only=('code_name',))
    #     )
    # )

    # @validates('name')
    # def validate_name(self, name):
    #     if re.match('^[a-zA-Z0-9_-]+$', name) is None:
    #         raise ValidationError(
    #             'A group\'s name can only contain valid characters.'
            # )
