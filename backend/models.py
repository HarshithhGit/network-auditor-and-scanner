from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class ScanResult(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target_ip = Column(String, index=True)
    port = Column(Integer)
    service = Column(String, nullable=True)
    status = Column(String, default="open")
    scanned_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String, index=True) # Low, Medium, High, Critical
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
