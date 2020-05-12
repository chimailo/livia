from sqlalchemy import exc
from flask import jsonify, request, url_for, current_app, Blueprint
from marshmallow import ValidationError

from app import db
from app.models import User
from app.schema import UserSchema
from app.errors import not_found, bad_request, error_response
# from app.utils.decorators import authenticate


users = Blueprint('users', __name__, url_prefix='/api')


@users.route('/users/ping', methods=['GET'])
def ping():
    """Test route for the admin blueprint."""
    return {
        'message': 'Users route!'
    }


@users.route('/users/page/<int:page>', methods=['GET'])
@users.route('/users', methods=['GET'])
# @permission_required(['can_view_user'])
def get_users(page=1):
    """Get list of users"""
    users = User.query.paginate(
        page,
        current_app.config['ITEMS_PER_PAGE'],
        False
    )
    next_url = url_for('users.get_users', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('users.get_users', page=users.prev_num) \
        if users.has_prev else None

    return {
        'items': UserSchema(many=True).dump(users.items),
        'next_url': next_url,
        'prev_url': prev_url
    }


@users.route('/users/<int:id>', methods=['GET'])
# @permissiousersn_required(['can_view_user'])
def get_user(id):
    """Get a single user"""
    user = User.find_by_id(id)
    if user is None:
        return not_found('User not found!')
    return jsonify(UserSchema().dump(user))


@users.route('/users', methods=['POST'])
# @permission_required(['can_add_user'])
def add_user():
    request_data = request.get_json()

    if not request_data:
        return bad_request("No input data provided")

    try:
        data = UserSchema().load(request_data)
    except ValidationError as err:
        return error_response(422, err.messages)

    try:
        # check for existing user
        email = User.find_by_identity(data.get('email'))
        username = User.find_by_identity(data.get('username'))

        if email is None and username is None:
            # add new user to db
            user = User()
            user.firstname = data.get('firstname')
            user.lastname = data.get('lastname')
            user.username = data.get('username')
            user.email = data.get('email')
            user.password = data.get('password')
            user.bio = data.get('bio')

            user.save()

            response = jsonify({
                'message': 'Successfully added new user.',
            })
            response.status_code = 201
            response.headers['Location'] = url_for(
                'users.get_user', id=user.id)
            return response
        else:
            return bad_request('Sorry. That user already exists.')

    # handle errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return error_response(500, 'Something went wrong, please try again.')


@users.route('/users/<int:id>', methods=['PUT'])
# @permission_required(['can_update_user'])
def update_user(id):
    request_data = request.get_json()

    if not request_data:
        return bad_request("No input data provided")

    try:
        data = UserSchema().load(request_data)
    except ValidationError as err:
        return error_response(422, err.messages)

    try:
        user = User.find_by_id(id)
        same_user = User.find_by_identity(data.get('username'))

        if same_user is None or same_user.username == user.username:
            # update user
            user.firstname = data.get('firstname')
            user.lastname = data.get('lastname')
            user.username = data.get('username')
            user.bio = data.get('bio')

            user.save()

            response = jsonify({
                'message': f'Successfully updated user.',
            })
            response.status_code = 200

            return response
        else:
            return bad_request(f'A user with that username already exists.')

    # handle errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return bad_request('Something went wrong, please try again.')


@users.route('/users/<int:id>', methods=['DELETE'])
# @permission_required(['can_delete_user'])
def delete_user(id):
    try:
        user = User.find_by_id(id)

        if user is None:
            return bad_request('User does not exist.')

        user.delete()
        return jsonify({'message': 'Successfully deleted user.'})
    except Exception as e:
        return jsonify({'message': e.message})
