from sqlalchemy import exc
from marshmallow import ValidationError
from flask import Blueprint, jsonify, request, url_for

# from app import db
# from app.api.models import User
# from app.api.schema import UserSchema
# from app.api.decorators import authenticate
# from app.api.errors import error_response, bad_request


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/ping', methods=['GET'])
def ping():
    return {
        'message': 'Auth Route!'
    }


# @auth.route('/check-username', methods=['POST'])
# def check_username():
#     req = request.get_json()
#     user = User.find_by_identity(req['username']) \
#         if 'username' in req else None
#     return {'res': not isinstance(user, User)}


# @auth.route('/check-email', methods=['POST'])
# def check_email():
#     req = request.get_json()
#     user = User.find_by_identity(req['email']) \
#         if 'email' in req else None
#     return {'res': not isinstance(user, User)}


# @auth.route('/register', methods=['POST'])
# def register_user():
#     request_data = request.get_json()

#     if not request_data:
#         return bad_request("No input data provided")

#     try:
#         data = UserSchema().load(request_data)
#     except ValidationError as err:
#         print(err)
#         return error_response(422, err.messages)

#     email = data['email']
#     password = data['password']
#     username = data['username'] if 'username' in data else None

#     try:
#         # check for existing user
#         user = User.query.filter(
#             (User.username == username) | (User.email == email)
#         ).first()

#         if user:
#             return bad_request('Sorry. That user already exists.')

#         # add new user to db
#         user = User(email=email, username=username, password=password)
#         user.save()

#         response = jsonify({
#             'message': 'Sign up was successful.',
#             'token': user.encode_auth_token(user.id).decode(),
#         })
#         response.status_code = 201
#         response.headers['Location'] = url_for(
#             'auth.get_user', id=user.id
#         )
#         return response

#     # handle errors
#     except (exc.IntegrityError, ValueError):
#         db.session.rollback()
#         return bad_request('Invalid payload, please try again.')


# @auth.route('/login', methods=['POST'])
# def login_user():
#     request_data = request.get_json()

#     if not request_data:
#         return bad_request("No input data provided")

#     try:
#         data = UserSchema().load(request_data)
#         # check for existing user
#         user = User.find_by_identity(data['email'])

#         if user and user.check_password(data['password']):
#             return jsonify({
#                 'message': 'Successfully logged in.',
#                 'token': user.encode_auth_token(user.id).decode(),
#             })
#         else:
#             return bad_request('Incorrect email or password.')

#     except Exception:
#         return bad_request('Invalid payload, please try again.')


# @auth.route('/logout', methods=['GET'])
# @authenticate
# def logout_user(id):
#     return jsonify({'message': 'Successfully logged out.'})


# @auth.route('/user', methods=['GET'])
# @authenticate
# def get_user(id):
#     user = User.find_by_id(id)
#     return {'data': UserSchema().dump(user)}
