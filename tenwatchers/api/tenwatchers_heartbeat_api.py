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

    def get(self, uid=None):
        if uid:
            return [u.to_json() for u in HeartbeatModel.query(uid)]
        return [u.to_json() for u in HeartbeatModel.query.all()]

    def post(self, uid):
        latitude = request.json.get('latitude', 0.0)
        longitude = request.json.get('longitude', 0.0)
        message = request.json.get('message')
        phone = request.json.get('phone')

        user = UserModel.query.get_or_404(uid)

        heartbeat = HeartbeatModel(
            message=message,
            user=user.id,
            receiver=phone,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(heartbeat)
        db.session.commit()
        return {
            "heartbeat_id": heartbeat.id
        }

    def put(self, uid):
        status = request.json.get('status')
        user = UserModel.query.get_or_404(uid)
        heartbeat = HeartbeatModel.query.filter_by(user=user.id).first()
        print heartbeat.to_json()
        heartbeat.update_status(False)
        db.session.commit()
        return {
            "status": status,
            'user': user.id
        }

api.add_resource(Heartbeat, '/heartbeat', '/heartbeat/<string:uid>')
