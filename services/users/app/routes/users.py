from flask import jsonify, request, url_for, current_app, Blueprint
# from sqlalchemy import exc
# from marshmallow import ValidationError

# from app import db
# from app.api.models import User
# from app.api.schema import UserSchema
# from app.api.errors import not_found, bad_request, error_response
# from app.api.decorators import authenticate
# from app.api.routes import admin


users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/ping', methods=['GET'])
def ping():
    """Test route for the admin blueprint."""
    return {
        'message': 'Admin route!'
    }


# @admin.route('/users/page/<int:page>', methods=['GET'])
# # @permission_required(['can_view_user'])
# def get_users(page):
#     """Get all users"""
#     users = User.query.paginate(
#         page,
#         current_app.config['ITEMS_PER_PAGE'],
#         False
#     )
#     next_url = url_for('admin.get_users', page=users.next_num) \
#         if users.has_next else ''
#     prev_url = url_for('admin.get_users', page=users.prev_num) \
#         if users.has_next else ''

#     return {
#         'items': UserSchema(many=True).dump(users.items),
#         'next_url': next_url,
#         'prev_url': prev_url
#     }


# @admin.route('/user/<int:id>', methods=['GET'])
# # @permissiousersn_required(['can_view_user'])
# def get_user(id):
#     """Get a single user"""
#     print(request.url_rule)
#     user = User.find_by_id(id)
#     if user is None:
#         return not_found('User not found!')
#     return jsonify(UserSchema().dump(user))


# @admin('/users', methods=['POST'])
# # @permission_required(['can_add_user'])
# def add_user():
#     request_data = request.get_json()

#     if not request_data:
#         return bad_request("No input data provided")

#     try:
#         data = UserSchema().load(request_data)
#     except ValidationError as err:
#         return error_response(422, err.messages)

#     try:
#         # check for existing user
#         existing_user = User.find_by_identity(data['email'])

#         if not existing_user:
#             # add new user to db
#             user = User(email=data['email'])
            
#             user.save()

#             response = jsonify({
#                 'message': 'Successfully added new user.',
#             })
#             response.status_code = 201
#             response.headers['Location'] = url_for(
#                 'admin.get_user', id=user.id)
#             return response
#         else:
#             return bad_request('Sorry. That user already exists.')

#     # handle errors
#     except (exc.IntegrityError, ValueError):
#         db.session.rollback()
#         return bad_request('Invalid payload, please try again.')



# @admin('/users', methods=['PUT'])
# # @permission_required(['can_update_user'])
# def update_user():
#     request_data = request.get_json()

#     if not request_data:
#         return bad_request("No input data provided")

#     try:
#         data = PermissionSchema().load(request_data)
#     except ValidationError as err:
#         return error_response(422, err.messages)

#     email = data['email']
#     username =  data['username']
#     user_groups = data['groups']
#     user_perms = data['perms']

#     try:
#         # check if user exists
#         user_to_update = User.find_by_id(id)

#         # check if a user with the new email already exist.
#         existing_user = User.find_by_identity(email) or User.find_by_identity(username)
        
#         if not existing_user:
#             user_to_update.username = username
#             user_to_update.email = email
#             user_to_update.user_groups = user_groups
#             user_to_update.user_perms = user_perms

#             user_to_update.save()

#             response = jsonify({
#                 'message': f'Successfully updated user.',
#             })
#             response.status_code = 200

#             return response
#         else:
#             return bad_request(f'That user already exist. Please use a different email')

#     # handle errors
#     except (exc.IntegrityError, ValueError):
#         db.session.rollback()
#         return bad_request('Something went wrong, please try again.')


# @admin.route('/users/<int:id>', methods=['DELETE'])
# # @permission_required(['can_delete_user'])
# def delete_user(id):
#     try:
#         user = User.find_by_id(id)
#         user.delete()
#     except Exception as e:
#         return jsonify({
#             'message': e.message
#         })
    