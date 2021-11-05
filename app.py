import os
import sys
cur_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, cur_dir + "/src")

from flask_websocket_ng import create_app

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = create_app()

if __name__ == '__main__':
	#os.environ['FLASK_ENV'] = 'development'

	app.debug = True
	server = pywsgi.WSGIServer(('127.0.0.1', 8080), app, handler_class=WebSocketHandler)
	server.serve_forever()
