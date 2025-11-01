from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.database import Base

class TriageRecord(Base):
    __tablename__ = "triage_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    symptoms = Column(Text)
    detected_symptoms = Column(Text)
    severity_label = Column(String)
    priority = Column(Integer)
    status = Column(String, default="waiting")
    timestamp = Column(DateTime, default=datetime.utcnow)
