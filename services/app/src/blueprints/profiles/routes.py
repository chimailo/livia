from flask import jsonify, request, Blueprint
from marshmallow import ValidationError

from src.utils.decorators import authenticate
from src.blueprints.errors import error_response, bad_request
from src.blueprints.auth.models import User
from src.blueprints.profiles.models import Profile
from src.blueprints.auth.schema import UserSchema
from src.blueprints.profiles.schema import ProfileSchema


profile = Blueprint('profile', __name__, url_prefix='/api')


@profile.route('/profile/check-username', methods=['POST'])
@authenticate
def check_username(id):
    data = request.get_json()
    profile = Profile.find_by_username(data.get('username'))

    if profile is not None:
        if profile.user_id != id:
            return {'res': False}

    return {'res': True}


@profile.route('/profile', methods=['GET'])
@authenticate
def get_profile(id):
    user = User.find_by_id(id)
    return {
        'user': UserSchema(
            exclude=(
                'current_sign_in_ip',
                'current_sign_in_on',
                'last_sign_in_ip',
                'last_sign_in_on',
                'sign_in_count',
                'updated_on',
                'created_on',
            )
        ).dump(user),
        'profile': ProfileSchema(
            exclude=('id', 'created_on', 'updated_on',)
        ).dump(user.profile)
    }


@profile.route('/profile', methods=['PUT'])
@authenticate
def update_profile(id):
    request_data = request.get_json()

    if not request_data:
        return bad_request("No input data provided")

    try:
        data = ProfileSchema().load(request_data)
    except ValidationError as error:
        return error_response(422, error.messages)

    try:
        user = User.find_by_id(id)
        profile = Profile.find_by_id(user.profile.id)

        profile.firstname = data.get('firstname').title()
        profile.lastname = data.get('lastname').title()
        profile.bio = data.get('bio')

        prof = Profile.find_by_username(data.get('username'))

        if prof is not None:
            if prof.user_id != id:
                return bad_request('Username is already taken.')

        profile.username = data.get('username')
        profile.save()

        response = jsonify({'message': 'Successfully updated your profile'})
        response.status_code = 200

        return response

    except Exception:
        return error_response(500, 'Something went wrong, please try again.')


@profile.route('/profile', methods=['DELETE'])
@authenticate
def delete_profile(id):
    try:
        user = User.find_by_id(id)
        user.delete()

        response = jsonify({'message': 'Successfully deleted your account'})
        response.status_code = 200

        return response
    except Exception:
        return error_response(500, 'Something went wrong, please try again.')
