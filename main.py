# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# ✅ Load DB + models BEFORE create_all()
from app.core.database import Base, engine
import app.models.user
import app.models.triage_record

# ✅ Now create tables
Base.metadata.create_all(bind=engine)

# ✅ Import routers AFTER loading models
from app.routes import triage, patients, auth, chat

app = FastAPI(
    title="AI-Powered Emergency Triage Assistant",
    version="1.0.0",
    description="Backend API for patient intake and severity scoring."
)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register API routes
app.include_router(auth.router)
app.include_router(triage.router)
app.include_router(patients.router)
app.include_router(chat.router)

# ✅ Custom Swagger / JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply JWT to all routes
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}
