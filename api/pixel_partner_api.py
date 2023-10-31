from flask import Blueprint, request, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS
import requests  # used for testing 
import random
import os

from model.pixel_partner_func import *
from model.pixel_partner_history import *

pixel_partner_api = Blueprint('pixel_partner_api', __name__,
                   url_prefix='/api/pixel-partner-api')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(pixel_partner_api)
CORS(pixel_partner_api, resources={r"/api/*": {"origins": "*"}})
# Uncomment above line for local testing
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
            print(data['addToHistory'])
            if data['addToHistory']:
                createImage(data['filename'], 'pixelate', imageToBase64(pixelated_image)) # adds to database
            return response
        
    class _Combine(Resource):
        def post(self):
            data = request.get_json()
            print(data)
            combined_image = combine(data['base64image1'], data['base64image2'], data['direction'])
            response = jsonify({"base64image": combined_image})
            if data['AddToHistory']:
                createImage(data['filename'], 'combine', imageToBase64(combined_image)) # adds to database
            return response
        
    class _GetDatabase(Resource):
        def get(self):
            # Debugging
            # debugDatabase()
            return queryImages()
        
    class _AddImage(Resource):
        def post(self):
            data = request.get_json()
            createImage(data["Name"], data["Function"], data["Base64Image"])
            
    class _ClearDatabase(Resource):
        def get(self):
            clearDatabase()

    # Colorscale functions
    class _Colorscale(Resource):
        def post(self):
            data = request.get_json() 
            colored_image = colorscale(base64toImage(data['Base64Image']), tuple([int(data['R']), int(data['G']), int(data['B'])]))
            response = jsonify({"Base64Image": imageToBase64(colored_image)})
            if data['addToHistory']:
                createImage(data['filename'], 'colorscale', imageToBase64(colored_image)) # adds to database
            return response

    #Grayscale
    class _Grayscale(Resource):
        def post(self):
            data = request.get_json() 
            colored_image = grayscale(base64toImage(data['Base64Image']))
            response = jsonify({"Base64Image": imageToBase64(colored_image)})
            if data['addToHistory']:
                createImage(data['filename'], 'greyscale', imageToBase64(colored_image)) # adds to database
            return response

    api.add_resource(_Test, '/test')
    api.add_resource(_Pixelate, '/pixelate/')
    api.add_resource(_Combine, '/combine/')
    api.add_resource(_GetDatabase, '/get_database')
    api.add_resource(_AddImage, '/add_image')
    api.add_resource(_ClearDatabase, '/clear_database')
    api.add_resource(_Colorscale, '/colorscale')
    api.add_resource(_Grayscale, '/grayscale')
