import flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit

from werkzeug.serving import make_server
import secrets

from threading import Thread, Timer

import os

from typing import Any, Iterable

import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def type_mapping(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, Iterable):
        if isinstance(value[0], int):
            return "list_int"
        elif isinstance(value[0], float):
            return "list_float"
        else:
            return "list"
    else:
        return "unknown"


class SocketServer:
    def __init__(
        self,
        port: int = 8080,
        host: str = "127.0.0.1",
        name: str = "TorchBoard",
        static_path: str = "torchboard/dist",
        board: Any = None,
        rate_limit_ms: int = 250,
    ) -> None:
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")
        from torchboard.base.board import Board

        self.port = port
        self.host = host
        self.static_path = static_path

        self.board: Board = board
        if self.board is None:
            raise ValueError("Board is not provided")
        
        self.rate_limit_ms = rate_limit_ms
        self.send_timer = None

        self.app = flask.Flask(name)
        self.app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

        self.__flask_process = None

        CORS(
            self.app, resources={r"/*": {"origins": "*"}}
        )  # TODO: Change origins to specific domain

        @self.app.route('/')
        def index():
            return flask.send_from_directory(self.static_path, 'index.html')

        @self.app.route('/<path:path>')
        def static_proxy(path):
            return flask.send_from_directory(self.static_path, path)
        
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.socketio.init_app(self.app)

        self.__config_socket()

        self.server = make_server(self.host, self.port, self.app, threaded=True)
        self.server.daemon_threads = True

    def start(self) -> None:
        if self.__flask_process:
            return
        self.__flask_process = Thread(target=self.server.serve_forever)
        self.__flask_process.daemon = True
        self.__flask_process.start()

        print(f"Started TorchBoard server at http://{self.host}:{self.port}")

    def stop(self) -> None:
        if not self.__flask_process:
            return
        self.__flask_process.join()
        self.__flask_process = None

    def __emit_to_channel(self, channel: str, data: Any,room=None):
        with self.app.app_context():
            if room is None:
                self.socketio.emit(channel, data)
            else:
                self.socketio.emit(channel, data, to=room)
    
    def emit_optimizer_variables(self, optim_operator, room=None):
        variables = [
            {"name": key, "value": value, "type": type_mapping(value)}
            for key, value in optim_operator.get_current_parameters().items()
        ]
        self.__emit_to_channel("getOptimizerVariables", variables, room=room)

    def emit_variable_values(self, history:dict[str,list[Any]], room=None):
        """
        Emit variable histories to the client
        """
        for key, value in history.items():
            self.__emit_to_channel("chartValueUpdate", {"key": key, "values": value}, room=room)
    
    def __emit_variable_changes(self, room=None):
        self.emit_variable_values(self.board.history.get_since_last_change(), room=room)
        self.send_timer = None
            
    def emit_variable_changes(self, room=None):
        """
        Emit chart variable changes to the client
        This function is rate limited to prevent spamming the client with socket updates in case of high frequency updates
        """
        if self.send_timer is not None:
            return
    
        
        self.send_timer = Timer(self.rate_limit_ms/1000, self.__emit_variable_changes, args=(room,))
        self.send_timer.start()
    
    def emit_board_variable_change(self, key:str, value:Any, room=None):
        self.__emit_to_channel("boardValueUpdate", {"key": key, "values": value}, room=room)
            
    def __config_socket(self):
        # This looks cursed ._.

        @self.socketio.on("connect")
        def connect():
            #print("Client connected", flask.request.sid)
            user_room = flask.request.sid
            try:
                self.emit_optimizer_variables(self.board.optim_operator, room=user_room)
            except AttributeError:
                pass
            #Send all history data only to newly connected client
            self.emit_variable_values(self.board.history.get_all(), room=user_room)
            self.emit_board_variable_change("training", self.board.do_training.is_set(), room=user_room)

        @self.socketio.on("disconnect")
        def disconnect():
            #print("Client disconnected", flask.request.sid)
            pass

        @self.socketio.on("actionTrigger")
        def actionTrigger(action_id, action_args):
            match action_id:
                case "toggle_training":
                    self.board.toggle_training()
                    self.emit_board_variable_change("training", self.board.do_training.is_set())
                case "save_model":
                    self.board.save_model()
                case _:
                    print(f"Unknown action: {action_id}")

        @self.socketio.on("optimizerValueUpdate")
        def optimizerValueUpdate(variable_name, value):
            self.board.optim_operator.update_parameters(variable_name, value)
            self.emit_optimizer_variables(self.board.optim_operator)
