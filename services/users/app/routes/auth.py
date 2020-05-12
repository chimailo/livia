from flask import Blueprint, jsonify, request, url_for
from sqlalchemy import exc
from marshmallow import ValidationError

from app import db
from app.errors import error_response, bad_request
from app.models import User
from app.schema import UserSchema
from app.utils.decorators import authenticate


auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.route('/ping', methods=['GET'])
def ping():
    return {'message': 'Auth Route!'}


@auth.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    user = User.find_by_identity(data.get('email'))
    return {'res': not isinstance(user, User)}


@auth.route('/check-username', methods=['POST'])
def check_username():
    data = request.get_json()
    user = User.find_by_identity(data.get('username'))
    return {'res': not isinstance(user, User)}


@auth.route('/register', methods=['POST'])
def register_user():
    print('request')
    request_data = request.get_json()

    if not request_data:
        return bad_request("No input data provided")

    try:
        data = UserSchema().load(request_data)
    except ValidationError as err:
        return error_response(422, err.messages)

    email = data.get('email')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    try:
        # check for existing user
        user = User.query.filter((User.email == email)).first()

        if user:
            return bad_request('Sorry. That user already exists.')

        # add new user to db
        user = User(email=email,
                    firstname=firstname,
                    lastname=lastname,
                    password=password)
        user.save()

        response = jsonify({
            'message': 'Sign up was successful.',
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
        return bad_request('Something went wrong, please try again.')


@auth.route('/login', methods=['POST'])
def login_user():
    request_data = request.get_json()

    if not request_data:
        return bad_request("No input data provided")

    try:
        data = UserSchema().load(request_data)
        # check for existing user
        user = User.find_by_identity(data.get('email'))
        user.update_activity_tracking()

        if user and user.check_password(data.get('password')):
            return jsonify({
                'message': 'Successfully logged in.',
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
    return {'data': UserSchema().dump(user)}
