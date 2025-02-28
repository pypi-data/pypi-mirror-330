from dataclasses import dataclass

from whisp.messages.WhispMessage import WhispMessage, whisp_message


@whisp_message(event="whisp/joined", description="Is sent when a client joined the network.", system_message=True)
@dataclass(slots=True)
class WhispJoined(WhispMessage):
    pass


@whisp_message(event="whisp/left", description="Is sent when a client left the network.", system_message=True)
@dataclass(slots=True)
class WhispLeft(WhispMessage):
    pass
