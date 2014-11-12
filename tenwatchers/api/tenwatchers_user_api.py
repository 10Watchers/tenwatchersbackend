#!/usr/bin/env python
from flask import Blueprint, request, abort, jsonify
from flask.ext.restful import Api, Resource
from tenwatchers.utils import json_response
from tenwatchers.util import send_sms
from tenwatchers.db import db
from tenwatchers.db.models import UserModel, Group, UserGroup


tenwatchers_user_api = Blueprint('tenwatchers_user_api', __name__)
api = Api(tenwatchers_user_api)


class Echo(Resource):
    method_decorators = [json_response]

    def get(self):
        return jsonify(
            {
                "App Status": "App is up and running",
            })

    def post(self):
        phone = request.json.get('phone')
        return send_sms(phone, 'hello world')

class User(Resource):
    method_decorators = [json_response]

    def get(self):
        return [u.to_json() for u in UserModel.query.all()]

    def post(self):
        password = request.json.get('password', "Foo")
        phone = request.json.get('phone')
        if password is None or phone is None:
            abort(400)    # missing arguments

        if UserModel.query.filter_by(
            phone=phone
        ).first() is not None:
            abort(409)    # existing user
        user = UserModel(phone=phone)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {
            "client_id": user.id
        }

class UserDetail(Resource):
    method_decorators = [json_response]

    def get(self, user_id):
        try:
            UserModel.query.get(user_id)
        except:
            abort(406)
        return {

        }

    def post(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(406)
        group = request.json.get("groupName")
        group = Group.query.filter_by(name = group).first()

        ug = UserGroup(
            user_id = user.id,
            group_id = group.id
        )
        alertThreshold = request.json.get("alertThreshold", 3)
        heartbeatAlertRecipientPhoneNumber = request.json.get("heartbeatAlertRecipientPhoneNumber")
        heartbeatAlertMessage = request.json.get("heartbeatAlertMessage")
        user.heartbeat_preference = heartbeatAlertRecipientPhoneNumber
        user.heartbeat_message = heartbeatAlertMessage
        user.message_theshold = alertThreshold

        db.session.add(user)
        db.session.add(ug)
        db.session.commit()

        return {
            "client_id": user.id
        }

api.add_resource(User, '/user')
api.add_resource(UserDetail, '/user/<string:user_id>')
api.add_resource(Echo, '/echo')
