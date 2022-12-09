from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class createAuthor(BaseModel):
    PID: int
    docID: int

class updateAuthor(BaseModel):
    PID: int
    docID: int