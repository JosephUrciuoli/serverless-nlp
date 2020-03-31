from dataclasses import dataclass, field
from typing import List


@dataclass
class Line:
    id: str
    text: str
    confidence: float
    page: int
    geometry: dict
    encoding: List[float] = field(default_factory=lambda: [])


@dataclass
class Document:
    lines: List[Line] = field(default_factory=lambda: [])
