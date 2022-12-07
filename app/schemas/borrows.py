from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class createBtxn(BaseModel):
    borNo: int
    docID: int
    copyID: int
    BID: int
    RID: int
    BDate: datetime
    Rdate: datetime

class updateBtxn(BaseModel):
    borNo: int
    docID: int
    copyID: int
    BID: int
    RID: int
    BDate: datetime
    Rdate: datetime
