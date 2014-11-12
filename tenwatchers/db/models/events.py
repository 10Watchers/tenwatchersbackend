from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from geoalchemy2 import Geometry

import geoalchemy2
from geoalchemy2.types import Geography

from tenwatchers.db import db

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)

    user_id = Column(db.VARCHAR(255), ForeignKey('user.id'), nullable=True)

    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    location = Column(Geography('POINT'), nullable=True)
    time = Column(DateTime, nullable=False)
    description = Column(Text)
    alert_level = Column(Integer, nullable=True)

    def update_location(self):
        """Update `self.location` with a point value derived from
          `self.latitude` and `self.longitude`.

          Note that the point will be `autocast`_ to geography type on saving:

          > Standard geometry type data will autocast to geography if it is of
            SRID 4326.

          `autocast`: http://postgis.refractions.net/docs/ch04.html#Geography_Basics
        """

        self.location = "POINT(%0.8f %0.8f)" % (self.long, self.lat)


    @classmethod
    def within_clause(cls, latitude, longitude, distance):
        """Return a within clause that explicitly casts the `latitude` and
          `longitude` provided to geography type.
        """

        attr = '%s.location' % cls.__tablename__

        point = 'POINT(%0.8f %0.8f)' % (longitude, latitude)
        location = "ST_GeographyFromText(E'SRID=4326;%s')" % point

        return 'ST_DWithin(%s, %s, %d)' % (attr, location, distance)

    @classmethod
    def intersects_clause(cls, json_polygon):
        """Return an intersects clause that accepts a geojson polygon as input
        """
        attr = '%s.location' % cls.__tablename__
        return "ST_Within({0})".format(json_polygon)

    def __repr__(self):
        return "%i Message from: %f, %f" % (self.active, self.lat, self.lon)
