from dataclasses import dataclass
from typing import Optional


@dataclass
class WhispConnection:
    sid: str
    name: Optional[str] = None
