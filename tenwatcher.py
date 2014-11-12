#!/usr/bin/env python
from __future__ import absolute_import
from flask import Flask
from tenwatchers.api.tenwatchers_user_api import tenwatchers_user_api
from tenwatchers.api.tenwatchers_heartbeat_api import tenwatchers_heartbeat_api
from tenwatchers.api.tenwatchers_groups_api import tenwatchers_groups_api
from tenwatchers.util import configure_logging
from default_settings import URL_PREFIX_VERSION
from tenwatchers.db import db


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object('default_settings')
    if config_module:
        app.config.from_object(config_module)
    # Loads a configuration from a configuration file the environment variable
    # ORCUS_SETTINGS points to.
    app.config.from_envvar('10WATCHERS_SETTINGS', silent=True)
    configure_logging(app)
    app.logger.info("Flask Application Started")
    app.logger.info("Setting up the API end points")

    app.register_blueprint(tenwatchers_user_api, url_prefix=URL_PREFIX_VERSION)
    app.register_blueprint(tenwatchers_heartbeat_api, url_prefix=URL_PREFIX_VERSION)
    app.register_blueprint(tenwatchers_groups_api, url_prefix=URL_PREFIX_VERSION)
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........

        if app.config.get("DROP_TABLES", False):
            app.logger.info("Dropping and recreating the database tables")
            db.drop_all()

        db.create_all()
    return app


app = create_app()

HOST = app.config['HOST']
PORT = app.config['PORT']

if __name__ == "__main__":

    app.run(host=HOST, port=PORT)
