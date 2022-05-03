from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    result = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
