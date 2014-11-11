from flask import Blueprint, jsonify
from flask.ext.restful import Api, Resource
from utils import json_response


apps_api = Blueprint('tenwatchers_api', __name__)
api = Api(apps_api)


class Echo(Resource):
    method_decorators = [json_response]

    def get(self):
        return jsonify(
            {
                "App Status": "App is up and running",
            })


api.add_resource(Echo, '/echo')
