from fastapi import APIRouter
from app.core.database import SessionLocal
from app.models.triage_record import TriageRecord

router = APIRouter(prefix="/patients", tags=["Doctor"])

@router.get("/")
def get_all_patients():
    db = SessionLocal()
    patients = db.query(TriageRecord).order_by(TriageRecord.timestamp.desc()).all()
    db.close()
    
    return [
        {
            "id": p.id,
            "patient_id": p.patient_id,
            "symptoms": p.symptoms,
            "severity": p.severity_label,
            "priority": p.priority,
            "status": p.status,
            "timestamp": p.timestamp
        }
        for p in patients
    ]
