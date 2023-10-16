from flask import Blueprint, request, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import random

from model.pixel_partner_func import *

pixel_partner_api = Blueprint('pixel_partner_api', __name__,
                   url_prefix='/api/pixel-partner-api')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(pixel_partner_api)

class PixelPartnerAPI:

    class _Test(Resource):
        def get(self):
            return jsonify({"Test": "Yay!"})

    class _Pixelate(Resource):
        def put(self):
            data = request.get_json()  # Get JSON data from the request
            pixelated_image = getTestPixel(data['base64image'])
            return jsonify({"Base-64": imageToBase64(pixelated_image)})

    api.add_resource(_Test, '/test')
    api.add_resource(_Pixelate, '/pixelate/')

if __name__ == "__main__": 
    server = "http://127.0.0.1:8017" # run local
    # server = 'https://fte.nighthawkcodingsociety.com' # run from web
    url = server + "/api/pixel-partner-api"
    
    request.get(url+"/test")
