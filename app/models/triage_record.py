from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class TriageRecord(Base):
    __tablename__ = "triage_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Patient data
    symptoms = Column(Text, nullable=True)               # comma-separated text
    duration = Column(String, nullable=True)
    severity_label = Column(String, nullable=False, default="Low")
    risk_factors = Column(Text, nullable=True)           # comma-separated text

    # Ticket / Queue
    ticket = Column(String, nullable=False)              # e.g., P1001 / A1030
    wait_time = Column(String, nullable=False)           # e.g., "Immediate", "20–40 minutes"
    status = Column(String, default="waiting")           # waiting | in-progress | done

    timestamp = Column(DateTime, default=datetime.utcnow)
