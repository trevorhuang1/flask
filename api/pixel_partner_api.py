from flask import Blueprint, request, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS
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
            response = jsonify({"Connection Test": "Successfully connected to backend!"})
            return response

    class _Pixelate(Resource):
        def post(self):
            data = request.get_json()  # Get JSON data from the request
            pixelated_image = pixelate(base64toImage(data['base64image']), int(data['pixelate_level']))
            response = jsonify({"base64image": imageToBase64(pixelated_image)})
            return response

    api.add_resource(_Test, '/test')
    api.add_resource(_Pixelate, '/pixelate/')

if __name__ == "__main__": 
    server = "http://127.0.0.1:8017" # run local
    # server = 'https://fte.nighthawkcodingsociety.com' # run from web
    url = server + "/api/pixel-partner-api"
