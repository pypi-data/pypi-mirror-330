import logging
import threading
from pathlib import Path
from typing import Any, Dict

from flask import Flask, request, Response, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

from whisp.messages.NetworkMessages import WhispJoined, WhispLeft
from whisp.server import _templates
from whisp.server.WhispConnection import WhispConnection
from ._templates import static
from .code import CODE_GENERATORS
from ..messages.WhispMessage import WHISP_MESSAGE_REGISTRY


class WhispServer:
    def __init__(self,
                 name: str = "Whisp Server",
                 host: str = "127.0.0.1",
                 port: int = 14000):
        self.name = name
        self.host = host
        self.port = port

        static_path = Path(static.__file__).parent
        template_path = Path(_templates.__file__).parent

        self.app = Flask(__name__, static_url_path="/static", static_folder=static_path, template_folder=template_path)
        self.app.logger.setLevel(level=logging.INFO)
        self.cors = CORS(self.app)

        self.socketio = SocketIO(self.app)

        self._setup_routes()
        self._setup_socket_io()

        self.connections: Dict[str, WhispConnection] = dict()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html.jinja",
                                   title=self.name,
                                   connections=self.connections)

        @self.app.route("/api/connections")
        def connections():
            return self.connections

        @self.app.route("/api/code/<language>")
        def code(language: str):
            code_generator = CODE_GENERATORS.get(language)
            if code_generator is None:
                return Response("The requested language is not implemented.",
                                status=404, mimetype="text/plain")

            code_generator = code_generator()
            messages = [m for m in WHISP_MESSAGE_REGISTRY if not m.system_message]
            code = code_generator.generate(messages)

            return Response(code, status=200, mimetype="text/plain")

    def _setup_socket_io(self):
        @self.socketio.on("connect")
        def handle_connect():
            sid = request.sid  # noqa
            self.connections[sid] = WhispConnection(sid)
            self.app.logger.info(f"client connected")

        @self.socketio.on("disconnect")
        def handle_disconnect():
            sid = request.sid  # noqa
            connection = self.connections.pop(sid)

            if connection.name is not None:
                self.socketio.emit(WhispLeft.event,
                                   WhispLeft(sender=connection.name).to_dict(), include_self=False)
            self.app.logger.info(f"client disconnected")

        @self.socketio.on("*")
        def handle_all_messages(event: str, data: Any):
            sid = request.sid  # noqa
            self.app.logger.info(f"message: {event} received: {data} sid: {sid}")
            self.socketio.emit(event, data, skip_sid=sid, include_self=False)

            # handle custom events
            if event == WhispJoined.event:
                message = WhispJoined.from_dict(data)
                self.connections[sid].name = message.sender

    def run(self):
        self.socketio.run(self.app, host=self.host, port=self.port, debug=True, allow_unsafe_werkzeug=True)

    def run_async(self) -> threading.Thread:
        thread = threading.Thread(name="whisp-server", target=self.run, daemon=True)
        thread.start()
        return thread
