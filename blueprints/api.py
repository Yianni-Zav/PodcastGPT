from flask import (Blueprint, 
                   request, 
                   jsonify, 
                   current_app, 
                   send_file, 
                    url_for,
                   make_response)
from flask.views import MethodView
from os import path, environ
from flask_cors import CORS, cross_origin


cast_api = Blueprint('cast_api', __name__)

# this is a dummy mock method until we have the actual podcast generator
def get_podcast(guest, host, topic, duration):
    print(f'GENERATING PODCAST:')
    print(f'\t GUEST:{guest},')
    print(f'\t HOST:{host},')
    print(f'\t TOPIC:{topic},')
    print(f'\t DURATION:{duration},')
    return f'JoeRoganBenShapiro.mp4'


class CastAPI(MethodView):
    # GET: 
    # Returns the list of available personalities, and their images 
    @cross_origin()
    def get(self):
        personalities = current_app.config['PERSONALITIES']
        # we need to make a mapping from personalities to their images
        # the images will be named the exact same as the personalities
        # they will be stored in the static/profiles folder
        personality_profiles = { personality: url_for('static', filename=f'profiles/{personality}.jpg', _external=True) for personality in personalities }

        return jsonify(personality_profiles), 200
    

    # POST:
    # Takes the Guest Name. The Host name, and the topic
    # Request:
    # json: {
        # "guest": 'personality_1'
        # "host": 'personality_2'
        # "topic": 'topic'
        # 'duration': <minutes>
    #}

    # returns an MP4 of the generated podcast
    @cross_origin()
    def post(self):
        video_name = get_podcast(request.json['guest'], 
                                 request.json['host'], 
                                 request.json['topic'], 
                                 request.json['duration'])  
        video_path = path.join(current_app.config['PODCASTS_PATH'], video_name)
        if path.exists(video_path):
            body = {
                'guest': request.json['guest'],
                'host': request.json['host'],
                'topic': request.json['topic'],
                'duration': request.json['duration'],
                'video_url': url_for('static', filename=video_path.split('static/')[1], _external=True)
            }
            return make_response(body, 200)
        else:
            return jsonify({'error': 'Video not found'}), 404
    

cast_view = CastAPI.as_view('cast_api')
cast_api.add_url_rule('/cast', methods=['GET', 'POST'], view_func=cast_view)