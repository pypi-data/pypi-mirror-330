import logging
from dataclasses import dataclass, field
from typing import Dict, Type, Callable, Any, TypeVar

import socketio

from whisp.external.Event import Event
from whisp.messages.NetworkMessages import WhispJoined
from whisp.messages.WhispMessage import WhispMessage

# Configure a module-level logger.
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=WhispMessage)


@dataclass
class WhispMessageRegistration:
    message_type: Type[WhispMessage]
    event: Event[WhispMessage] = field(default_factory=Event)


@dataclass
class WebsocketMessage:
    event: str
    data: Any


class WhispClient:
    def __init__(
            self,
            name: str,
            address: str = "http://127.0.0.1:14000",
            auto_reconnect: bool = True,
    ):
        self.name = name
        self.address = address

        # Events to notify external listeners.
        self.on_connect = Event[WhispClient]()
        self.on_message = Event[WebsocketMessage]()
        self.on_disconnect = Event[WhispClient]()

        self.on_lynx_message: Event[WhispMessage] = Event()

        # Registry mapping message types to events.
        self._event_registry: Dict[str, WhispMessageRegistration] = dict()

        # Create the Socket.IO client with auto reconnection if enabled.
        self.sio = socketio.Client(reconnection=auto_reconnect)
        self._setup_socket_io()

    def register(self, message_type: Type[T], handler: Callable[[T], None]):
        """
        Register a handler for a specific LynxMessage type.
        """
        registration = self._event_registry.get(message_type.event)

        if registration is None:
            registration = WhispMessageRegistration(message_type)
            self._event_registry[message_type.event] = registration

        registration.event.append(handler)

    def connect(self):
        """
        Connect to the Socket.IO server.
        """
        try:
            logger.info(f"[{self.name}] Attempting to connect to {self.address}")
            self.sio.connect(self.address, retry=True)

            # after connecting - send joined message (updates client id)
            self.send(WhispJoined())
        except Exception as e:
            logger.error(f"[{self.name}] Failed to connect: {e}")

    def disconnect(self):
        """
        Gracefully disconnect from the Socket.IO server.
        """
        try:
            logger.info(f"[{self.name}] Disconnecting from websocket server at {self.address}")
            self.sio.disconnect()
        except Exception as e:
            logger.error(f"[{self.name}] Error during disconnect: {e}")

    def send(self, message: WhispMessage):
        # set client if not already set
        if message.sender is None:
            message.sender = self.name

        # deserialize message
        data = message.to_dict()

        # send message
        self.sio.emit(message.event, data)

    def _setup_socket_io(self):
        """
        Setup the Socket.IO client event handlers for connection, disconnection,
        and incoming messages.
        """

        @self.sio.event
        def connect():
            logger.info(f"[{self.name}] Connected to websocket server at {self.address}")
            self.on_connect(self)

        @self.sio.event
        def disconnect():
            logger.info(f"[{self.name}] Disconnected from websocket server at {self.address}")
            self.on_disconnect(self)

        @self.sio.on("*")
        def on_message(event: str, data: Any):
            message = WebsocketMessage(event, data)
            logger.info(f"[{self.name}] Received websocket message: {message}")
            self.on_message(message)
            self._handle_message(message)

    def _handle_message(self, ws_message: WebsocketMessage):
        # check if message is registered
        registration = self._event_registry.get(ws_message.event)
        if registration is None:
            return

        # handle registered message
        whips_message = registration.message_type.from_dict(ws_message.data)
        registration.event(whips_message)
