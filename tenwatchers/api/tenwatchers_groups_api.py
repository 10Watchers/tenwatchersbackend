#!/usr/bin/env python
from flask import Blueprint, request, abort, jsonify
from flask.ext.restful import Api, Resource
from tenwatchers.utils import json_response
from tenwatchers.db import db
from tenwatchers.db.models import UserGroup, Group, UserModel


tenwatchers_groups_api = Blueprint('tenwatchers_groups_api', __name__)
api = Api(tenwatchers_groups_api)


class UserGroups(Resource):
    method_decorators = [json_response]

    def get(self, user_id):
        try:
            user = UserModel.query.get(user_id)
        except: #TODO Does not exist
            abort(406)# bad request

        return [g.name for g in user.groups.all()]

    def post(self, user_id):
        try:
            user = UserModel.query.get(user_id)
        except: #TODO Does not exist
            abort(406)# bad request

        groups = request.json.get("groups", [])
        for g in groups:
            new_group = UserGroup.query.filter(name=g).first()
            if not new_group:
                new_group = UserGroup(name=g)
                session.db.add(new_group)
                session.save()
            user.groups.add(new_group)

        return {
            "success" : True
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

api.add_resource(UserGroups, '/user/groups/<string:user_id>')
api.add_resource(Groups, '/group')
