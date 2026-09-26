"""
Central configuration for the backend.

All values are read from environment variables (see .env.example at the
project root). Never hardcode secrets, API keys, or credentials here --
that is exactly the mistake the "Cloud Security" section of this project
warns against.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Auth / JWT ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-only-secret-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # --- Database ---
    # Defaults to a local SQLite file so the project runs with zero setup.
    # For a real cloud deployment, point this at a managed database instead,
    # e.g. postgresql://user:pass@host:5432/dbname (Supabase / Neon / Cloud SQL).
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./diet_planner.db")

    # --- Cloud storage (simulated locally) ---
    # For a real deployment, swap cloud/storage_service.py to write to
    # Firebase Storage / AWS S3 / GCS instead of the local filesystem.
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./storage/uploads")

    # --- CORS ---
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

    # --- Optional external AI API (Version B diet engine) ---
    # If unset, the AI engine automatically falls back to the local
    # rule-based recommendation engine (Version A) -- see ai_engine/diet_engine.py
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")


settings = Settings()
