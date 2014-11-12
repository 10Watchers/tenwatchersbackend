#!/usr/bin/env python
from flask import Blueprint, request, abort, jsonify
from flask.ext.restful import Api, Resource
from tenwatchers.utils import json_response
from tenwatchers.db import db
from tenwatchers.db.models import UserModel, UserGroup, Group, HeartbeatModel


tenwatchers_api = Blueprint('tenwatchers_api', __name__)
api = Api(tenwatchers_api)


class Echo(Resource):
    method_decorators = [json_response]

    def get(self):
        return jsonify(
            {
                "App Status": "App is up and running",
            })


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

class UserGroups(Resource):
    method_decorators = [json_response]

    def get(self, user_id):
        try:
            user = User.query.get(user_id)
        except: #TODO Does not exist
            abort(406)# bad request

        return [g.name for g in user.groups.all()]

    def post(self, user_id):
        try:
            user = User.query.get(user_id)
        except: #TODO Does not exist
            abort(406)# bad request

        groups = request.json.get("groups", [])
        for g in groups:
            new_group = Group.query.filter(name=g).first()
            if not new_group:
                new_group = Group(name=g)
                session.db.add(new_group)
                session.save()
            user.groups.add(group)

        return {
            "success" : True
        }



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


class Groups(Resource):
    method_decorators = [json_response]

    def get(self):
        return [{"id" : g.id, "name": g.name } for g in Group.query.all()]

    def post(self):
        created = False
        name = request.json.get('name')
        id = request.json.get('id', None)
        if id:
            try:
                group = Group.query.get(id)
            except: #TODO: only catch Does Not Exist exceptions
                abort(406) # No group with that id
        else:
            group = Group.query.filter_by(name=name).first()
        if not group:
            group = Group(id = id)
            created = True
        group.name = name
        db.session.add(group)
        db.session.commit()
        return jsonify({
            "group_id" : group.id,
            "group" : group.name,
            "created" : created
        })

api.add_resource(Echo, '/echo')
api.add_resource(User, '/user')
api.add_resource(UserGroups, '/user/groups/<string:user_id>')
api.add_resource(Groups, '/group')
api.add_resource(Heartbeat, '/heartbeat')
