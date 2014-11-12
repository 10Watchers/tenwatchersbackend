#!/usr/bin/env python
from tenwatchers.db import db
from tenwatchers.util import generate_uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, VARCHAR, Boolean, Float

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
    action = Column(Integer)

    def __init__(
            self,
            user,
            latitude,
            longitude,
            updated_time=None,
            expire_time=None,
            status=None,
            action=None
    ):
        self.id = generate_uuid()
        self.user = user
        self.latitude = latitude
        self.longitude = longitude
        self.location = "POINT(%0.8f %0.8f)" % (self.longitude, self.latitude)
        self.created_time = datetime.utcnow()
        self.updated_time = updated_time
        self.expire_time = datetime.utcnow()

    def __repr__(self):
        return "Heartbeat from: {0}".format(self.user)

    def to_json(self):
        json_heartbeat = {
            'id': self.id,
            'action': self.action,
            'location': str(self.location),
            'created_time': str(self.created_time),
            'expire_time': str(self.expire_time),
            'user': self.user
        }
        return json_heartbeat
