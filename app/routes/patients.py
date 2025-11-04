# backend/app/routes/patients.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db

router = APIRouter(prefix="/patients", tags=["Doctor"])

@router.get("/")
def get_all_patients(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ensure only authenticated users (doctor) access
):
    # Lazy import — avoids circular imports during app startup
    from app.models.triage_record import TriageRecord

    patients = (
        db.query(TriageRecord)
        .order_by(TriageRecord.timestamp.desc())
        .all()
    )

    return [
        {
            "id": p.id,
            "patient_id": p.patient_id,
            "symptoms": p.symptoms,
            "severity": p.severity_label,
            "priority": None,  # legacy key placeholder
            "status": p.status,
            "ticket": p.ticket,
            "wait_time": p.wait_time,
            "timestamp": p.timestamp
        }
        for p in patients
    ]
