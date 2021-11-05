import typing as t

from werkzeug.routing import Map, Rule, WebsocketMismatch
from werkzeug.exceptions import NotFound
from werkzeug.http import parse_cookie
from flask import request
from flask import _request_ctx_stack

# Monkeys are made for freedom.
try:
    from geventwebsocket.gunicorn.workers import GeventWebSocketWorker as Worker
    from geventwebsocket.handler import WebSocketHandler
    from gunicorn.workers.ggevent import PyWSGIHandler

    import gevent
except ImportError:
    pass

class Websocket(object):

    def __init__(self, app):
        self.app = app
        self.app_wsgi_app = app.wsgi_app
        app.wsgi_app = self.wsgi_app

    def wsgi_app(self, environ: dict, start_response: t.Callable) -> t.Any:
        adapter = self.app.url_map.bind_to_environ(environ)
        try:
            handler, values = adapter.match(websocket=True)
            w_socket = environ['wsgi.websocket']
            cookie = None
            if 'HTTP_COOKIE' in environ:
                cookie = parse_cookie(environ['HTTP_COOKIE'])

            with self.app.app_context():
                with self.app.request_context(environ):
                    # add cookie to the request to have correct session handling
                    request.cookie = cookie

                    req = _request_ctx_stack.top.request
                    rule = req.url_rule

                    self.app.ensure_sync(self.app.view_functions[rule.endpoint])(w_socket)

                    return []
        except (NotFound, KeyError, WebsocketMismatch):
            return self.app_wsgi_app(environ, start_response)


# CLI sugar.
if ('Worker' in locals() and 'PyWSGIHandler' in locals() and
        'gevent' in locals()):

    class GunicornWebSocketHandler(PyWSGIHandler, WebSocketHandler):
        def log_request(self):
            if '101' not in self.status:
                super(GunicornWebSocketHandler, self).log_request()

    Worker.wsgi_handler = GunicornWebSocketHandler
    worker = Worker

