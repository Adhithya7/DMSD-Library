from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class createBook(BaseModel):
    docID: int
    ISBN: int

class updateBook(BaseModel):
    docID: int
    ISBN: int
