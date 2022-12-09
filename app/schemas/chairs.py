from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class createchairs(BaseModel):
    PID: int
    docID: int

class updateChairs(BaseModel):
    PID: int
    docID: int