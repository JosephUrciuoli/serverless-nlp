"""

This module defines the Classes that can be leveraged by the action classes in
the rest of the project. A Document has many Lines. Each Line has attributes
around location, content, OCR extraction confidence, and it's encoding.

"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Line:
    """Definition of the Line object. Represents a line in a PDF document.

      Attributes:
          id: unique identifier of the line
          text: the text content on the line in the document
          confidence: textract confidence of the text OCR'd from the document
          page: the page in the document the line appears on
          geometry: precise character level location of line text
          encoding: the Bert encoding of the text

      """
    id: str
    text: str
    confidence: float
    page: int
    geometry: dict
    encoding: List[float] = field(default_factory=lambda: [])


@dataclass
class Document:
    """Definition of the Document object. Represents a PDF document.

      Attributes:
          line: list of lines in the document. each line contains metadata in the Line object

      """
    lines: List[Line] = field(default_factory=lambda: [])
