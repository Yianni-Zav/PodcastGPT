from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView

cast_api = Blueprint('cast_api', __name__)

class CastAPI(MethodView):


    # GET: 
    # Returns the list of available personalities, and their images 
    def get(self):
        return 'Testing Get'
    

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
    def post(self):
        pass
    

cast_view = CastAPI.as_view('cast_api')
cast_api.add_url_rule('/cast', methods=['GET', 'POST'], view_func=cast_view)