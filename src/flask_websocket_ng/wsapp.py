from flask import Flask, Blueprint

bp = Blueprint('ws', __name__)

@bp.route('/echo', websocket = True)
def echo(socket):
    while not socket.closed:
        message = "Echo: " + socket.receive()
        socket.send(message)