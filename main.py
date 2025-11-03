from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routes import triage
from app.routes import triage, patients, auth, chat
from app.core.database import Base, engine

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

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

# ✅ Register routes
app.include_router(auth.router)
app.include_router(triage.router)
app.include_router(patients.router)
app.include_router(chat.router)
app.include_router(triage.router)

# ✅ Add Global Bearer Auth for Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    # ✅ Define JWT Bearer security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # ✅ Apply security globally (to all endpoints)
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"BearerAuth": []}
            ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}
