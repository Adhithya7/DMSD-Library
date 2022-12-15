from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class createDoc(BaseModel):
    docID: int
    ISBN: int

class createCopy(BaseModel):
    id: int