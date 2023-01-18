from flask import Blueprint, jsonify, Flask
from api.swagger import generator, swagger_destination_path, swaggerui_blueprint
from api.routes.users import users_router
from api.routes.chats import chats_router

app = Flask(__name__, static_folder='static')

app.register_blueprint(users_router)
app.register_blueprint(chats_router)
# TODO: Add more routers

generator.generate_swagger(app, destination_path=swagger_destination_path)

app.register_blueprint(swaggerui_blueprint)

app.run()
