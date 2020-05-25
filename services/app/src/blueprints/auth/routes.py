from flask import jsonify, request, url_for, Blueprint, request
from sqlalchemy import exc
from marshmallow import ValidationError

from src import db
from src.utils.decorators import authenticate
from src.blueprints.errors import error_response, bad_request
from src.blueprints.auth.models import User
from src.blueprints.profiles.models import Profile
from src.blueprints.auth.schema import UserSchema, AuthSchema
from src.blueprints.profiles.schema import ProfileSchema


auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.route('/ping', methods=['GET'])
def ping():
    return {'message': 'Auth Route!'}


@auth.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    user = User.find_by_email(data.get('email'))
    return {'res': not isinstance(user, User)}


@auth.route('/register', methods=['POST'])
def register_user():
    request_data = request.get_json()

    if not request_data:
        return bad_request("No input data provided")

    try:
        data = AuthSchema().load(request_data)
    except ValidationError as err:
        return error_response(422, err.messages)

    email = data.get('email')
    password = data.get('password')
    firstname = data.get('firstname').title()
    lastname = data.get('lastname').title()

    try:
        # check for existing user
        user = User.query.filter(User.email == email).first()

        if user:
            return bad_request('Sorry. That user already exists.')

        # add new user to db
        profile = Profile(firstname=firstname, lastname=lastname)
        profile.username = profile.set_username()
        profile.avatar = profile.set_avatar(email)

        user = User(email=email, password=password, profile=profile)
        user.save()

        response = jsonify({
            'token': user.encode_auth_token(user.id).decode(),
        })
        response.status_code = 201
        response.headers['Location'] = url_for(
            'auth.get_user', id=user.id
        )
        return response

    # handle errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return error_response(500, 'Something went wrong, please try again.')


@auth.route('/login', methods=['POST'])
def login_user():
    request_data = request.get_json()

    if request_data is None:
        return bad_request("No input data provided")

    try:
        data = AuthSchema(partial=True).load(request_data)

        # check for existing user
        user = User.find_by_email(data.get('email'))
        user.update_activity_tracking(request.remote_addr)

        if user and user.check_password(data.get('password')):
            return jsonify({
                'token': user.encode_auth_token(user.id).decode(),
            })
        else:
            return error_response(401, 'Incorrect email or password.')

    except Exception:
        return bad_request('Invalid payload, please try again.')


@auth.route('/logout', methods=['GET'])
@authenticate
def logout_user(id):
    return jsonify({'message': 'Successfully logged out.'})


@auth.route('/user', methods=['GET'])
@authenticate
def get_user(id):
    user = User.find_by_id(id)
    return {
        'user': UserSchema(
            only=('id', 'email', 'is_active', 'is_admin')
        ).dump(user),
        'profile': ProfileSchema(
            exclude=('id', 'updated_on', 'created_on')
        ).dump(user.profile)
    }


@auth.route('/reset-password', methods=['GET'])
@authenticate
def reset_password():
    pass
