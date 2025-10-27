from fastapi import FastAPI
from app.routes import triage

app = FastAPI(
    title="AI-Powered Emergency Triage Assistant",
    version="1.0.0",
    description="Backend API for patient intake and severity scoring."
)

# Include routes
app.include_router(triage.router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}
