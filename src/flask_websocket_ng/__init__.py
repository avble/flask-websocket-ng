import os
from threading import Thread

from flask import Flask

from . import flaskapp
from . import wsapp
from .middleware import websocket as ws

def create_app():
    app = Flask(__name__)
    # Apply middle-ware for handling websocket
    websock = ws.Websocket(app)
    app.register_blueprint(flaskapp.bp)
    app.register_blueprint(wsapp.bp)

    return app
