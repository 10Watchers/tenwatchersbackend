#!/usr/bin/env python
from flask import Blueprint, request
from flask.ext.restful import Api, Resource
from tenwatchers.utils import json_response
from tenwatchers.db import db
from tenwatchers.db.models import HeartbeatModel, UserModel


tenwatchers_heartbeat_api = Blueprint('tenwatchers_heartbeat_api', __name__)
api = Api(tenwatchers_heartbeat_api)


class Heartbeat(Resource):
    method_decorators = [json_response]

    def get(self):
        return [u.to_json() for u in HeartbeatModel.query.all()]

    #POST /heartbeat/uid/start

    def post(self):
        uid = request.json.get('uid')
        latitude = request.json.get('latitude', 0.0)
        longitude = request.json.get('longitude', 0.0)
        action = request.json.get('action')

        user = UserModel.query.get_or_404(uid)

        heartbeat = HeartbeatModel(
            action=action,
            user=user.id,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(heartbeat)
        db.session.commit()
        return {
            "heartbeat_id": heartbeat.id
        }

api.add_resource(Heartbeat, '/heartbeat')
