from flask import flask

from blueprints.api import cast_api
from os import path
from flask import Flask

app = Flask(__name__)

def construct_app():
    app_dir = path.dirname(path.realpath(__file__))
    app_name = path.basename(app_dir)

    app = Flask(app_name, root_path=app_dir) 

    app.register_blueprint(cast_api)