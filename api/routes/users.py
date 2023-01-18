from flask import Blueprint, render_template, abort, request
from startup import users
from api.auth import require_token
from api.swagger import generator
from flask_swagger_generator.utils import SecurityType
from flask_restplus import Api

users_blueprint = Blueprint('users', __name__)
users_router = Api(users_blueprint)

@generator.security(SecurityType.BEARER_AUTH)
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@generator.request_body({'id': 10, 'name': 'test_object'})
@require_token
@users_router.route('/users', methods=['GET'])
def get_users():
    return users.get_users(), 200

@generator.security(SecurityType.BEARER_AUTH)
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@generator.request_body({'id': 10, 'name': 'test_object'})
@users_router.route('/user/<id>', methods=['GET'])
def get_user(id: int):
    user = users.get_user(id)
    if not user:
        abort(404)
    return user, 200

@generator.security(SecurityType.BEARER_AUTH)
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@generator.request_body({'id': 10, 'name': 'test_object'})
@require_token
@users_router.route('/user', methods=['POST'])
def create_user():
    id = request.args.get('id')
    name = request.args.get('name')
    user = users.create_user(id, name)
    return user, 201

@generator.security(SecurityType.BEARER_AUTH)
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@generator.request_body({'id': 10, 'name': 'test_object'})
@require_token
@users_router.route('/user/<id>', methods=['PUT'])
def update_user(id: int):
    params = request.args.get('user')
    user = {} # TODO: update user by id with params
    if not user:
        abort(404)
    return user, 200

@generator.security(SecurityType.BEARER_AUTH)
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@generator.request_body({'id': 10, 'name': 'test_object'})
@require_token
@users_router.route('/user/<id>', methods=['DELETE'])
def delete_user(id: int):
    # TODO: delete user by id
    return '', 204