from typing import Optional
from pydantic import BaseModel
import datetime

class ReportBase(BaseModel):
    file_name: str
    result: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    created: datetime.datetime

    class Config:
        orm_mode = True
