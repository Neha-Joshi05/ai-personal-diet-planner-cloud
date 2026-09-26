"""
App entry point.

Run from the project root with:
    uvicorn backend.app:app --reload

This wires together every layer described in the architecture doc:
    Frontend -> REST API (this file's routers) -> services -> cloud/ -> database
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import init_db
from backend.routes import auth, profile, plans, files

app = FastAPI(
    title="AI-Powered Personal Diet Planner with Cloud Storage",
    description="Cloud Computing course project — see /docs for the live API reference.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "diet-planner-api"}


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(plans.router)
app.include_router(files.router)
