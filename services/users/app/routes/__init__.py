# from flask import Blueprint

# from app.api.decorators import status_required, authenticate


# admin = Blueprint('admin', __name__, url_prefix='/admin')


# @admin.before_request
# @authenticate
# @status_required
# def before_request():
#     """ Protect all of the admin endpoints. """
#     pass


# @admin.route('/ping', methods=['GET'])
# def ping():
#     """Test route for the admin blueprint."""
#     return {
#         'message': 'Admin route!'
#     }
