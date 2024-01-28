from flask import Blueprint, request, jsonify, send_from_directory
from flask.views import MethodView
from settings import CLIENT_DEV_PATH, STATIC_FOLDER_PATH


client_api = Blueprint('client_api', __name__)
client_api.static_folder = STATIC_FOLDER_PATH

class Client(MethodView):

    def get(self, path):
        print(client_api.static_folder)
        print(path)
        return send_from_directory(client_api.static_folder, f'client/{path}')
    



client_view = Client.as_view('client')
client_api.add_url_rule('/client/<path:path>', view_func=client_view, methods=['GET'])