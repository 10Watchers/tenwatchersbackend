#!/usr/bin/env python
from tenwatchers.db import db
from tenwatchers.util import generate_uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, VARCHAR, Boolean, Float, String

# import geoalchemy2
from geoalchemy2.types import Geography


class HeartbeatModel(db.Model):
    __tablename__ = 'heartbeat'
    id = Column(VARCHAR(255), primary_key=True)
    created_time = Column(DateTime, index=True)
    updated_time = Column(DateTime, index=True)
    expire_time = Column(DateTime, index=True)
    user = Column(
        VARCHAR(255),
        db.ForeignKey('user.id'),
        index=True)
    location = Column(Geography('POINT'))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(Boolean)
    receiver = Column(String(120))
    message = Column(VARCHAR(255))

    def __init__(
            self,
            user,
            latitude,
            longitude,
            updated_time=None,
            expire_time=None,
            status=True,
            receiver=None,
            message=None
    ):
        self.id = generate_uuid()
        self.user = user
        self.latitude = latitude
        self.longitude = longitude
        self.location = "POINT(%0.8f %0.8f)" % (self.longitude, self.latitude)
        self.status = status
        self.created_time = datetime.utcnow()
        self.updated_time = updated_time
        self.expire_time = datetime.utcnow()
        self.receiver = receiver
        self.message = message

    def __repr__(self):
        return "Heartbeat from: {0}".format(self.user)

    def update_status(self, status):
        self.status = False
        return self

    def to_json(self):
        json_heartbeat = {
            'id': self.id,
            'receiver': self.receiver,
            'action': 'Send: {0} to {1}'.format(self.message, self.receiver),
            'location': str(self.location),
            'created_time': str(self.created_time),
            'expire_time': str(self.expire_time),
            'user': self.user,
            'status': self.status
        }
        return json_heartbeat
