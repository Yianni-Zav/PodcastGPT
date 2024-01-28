from flask import Flask
import sys
from blueprints.api import cast_api
from blueprints.client import client_api
from os import path, environ
from flask import Flask
from flask_cors import CORS
import logging
from settings import *
import shutil

from API_Keys import NGROK_API_KEY

app = Flask(__name__)

if PORTWORD_TUNNEL_ON:
    from pyngrok import ngrok 
    try:
        ngrok.set_auth_token(NGROK_API_KEY)
        print('NGROK API KEY SET')
    except:
        print('NGROK API KEY FAILED')
        pass


def construct_app():

    global app  # Declare app as a global variable

    # copy dev client to static folder
    # if the folder already exists, remove it
    destination = f'{STATIC_FOLDER_PATH}/client/'
    if path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(CLIENT_DEV_PATH, destination)
    

    app_dir = path.dirname(path.realpath(__file__))
    app_name = path.basename(app_dir)

    app = Flask(app_name, root_path=app_dir) 

    CORS(app)

    app.register_blueprint(cast_api)
    app.register_blueprint(client_api)

    app.config.from_object('settings')

    # Logging
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    app.debug = True

    return app


app = construct_app()

if __name__ == '__main__':
    
    # tunnels = ngrok.get_tunnels()
    # http_tunnel = tunnels[0]
    # if len(tunnels) >= 1:
    # else:
    if PORTWORD_TUNNEL_ON:
      try:
          tunnels = ngrok.get_tunnels() 
          for tunnel in tunnels:
              ngrok.disconnect(tunnel.public_url)

          http_tunnel = ngrok.connect(app.config['APP_PORT'])
          print(f' * RUNNING ON {http_tunnel.public_url}/client/index.html')

          # we need to modify the js file to point to the ngrok url
          script_path = f'{STATIC_FOLDER_PATH}/client/script.js'
          orignal_text = "const SERVER_API_URL = 'http://localhost:5002';"
          new_text = f"const SERVER_API_URL = '{http_tunnel.public_url}';"
          with open(script_path, 'r') as f:
              script = f.read()
          script = script.replace(orignal_text, new_text)
          with open(script_path, 'w') as f:
              f.write(script)
      except:
          pass



    environ['FLASK_DEBUG'] = 'development'
    config = app.config

    try:
        app.run(debug=True,host='0.0.0.0', port=config['APP_PORT'], use_reloader=False)
    except KeyboardInterrupt:
        if PORTWORD_TUNNEL_ON:
            ngrok.disconnect(http_tunnel.public_url)
    finally:
      if PORTWORD_TUNNEL_ON:
          ngrok.disconnect(http_tunnel.public_url)
