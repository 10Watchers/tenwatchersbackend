#!/usr/bin/env python
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from tenwatchers.db import db
from flask import current_app
from tenwatchers.util import generate_uuid

from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from .events import Event

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.VARCHAR(255), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    phone = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    events = relationship("Event", backref="user")

    def __init__(
            self,
            phone=None,
            password_hash=None):
        self.id = generate_uuid()
        self.phone = phone
        self.password_hash = password_hash
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Username %r>' % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):  # 600 seconds = 10 minutes
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def to_json(self):
        json_user = {
            'phone': self.phone,
            'id': self.id
        }
        return json_user

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = UserModel.query.get(data['id'])
        return user


class UserGroup(db.Model):
    user_id = db.Column(db.VARCHAR(255), ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('group.id'), primary_key=True)
    user = relationship("UserModel", backref="user_groups")

class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    users = relationship("UserGroup", backref="groups")
