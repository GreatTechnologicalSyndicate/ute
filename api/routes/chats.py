from flask import Blueprint, render_template, abort, request
from startup import chats
from api.auth import require_token
from api.swagger import generator
from flask_swagger_generator.utils import SecurityType
from flask_restplus import Api

chats_blueprint = Blueprint('chats', __name__)
chats_router = Api(chats_blueprint)


@require_token
@chats_router.route('/chats', methods=['GET'])
def get_chats():
    return chats.get_chats(), 200

@chats_router.route('/chat/<id>', methods=['GET'])
def get_chat(id: int):
    chat = chats.get_chat(id)
    if not chat:
        abort(404)
    return chat, 200

@require_token
@chats_router.route('/chat', methods=['POST'])
def create_chat():
    id = request.args.get('id')
    title = request.args.get('title')
    chat = create_chat(id, title)
    return chat, 201

@require_token
@chats_router.route('/chat/<id>', methods=['PUT'])
def update_chat(id: int):
    params = request.args.get('chat')
    chat = {} # TODO: update chat by id with params
    if not chat:
        abort(404)
    return chat, 200

@require_token
@chats_router.route('/chat/<id>', methods=['DELETE'])
def delete_chat(id: int):
    chats.delete_chat(id)
    return '', 204