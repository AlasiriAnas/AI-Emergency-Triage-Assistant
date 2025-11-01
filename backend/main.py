from fastapi import FastAPI
from app.routes import triage, patients
from app.core.database import Base, engine
from app.models.triage_record import TriageRecord
from app.routes import auth


# ✅ Create database tables at startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Emergency Triage Assistant",
    version="1.0.0",
    description="Backend API for patient intake and severity scoring."
)

# ✅ Include routes
app.include_router(triage.router)
app.include_router(patients.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}
