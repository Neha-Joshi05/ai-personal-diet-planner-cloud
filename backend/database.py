"""
Database engine + session factory.

This is the "cloud database" of the project. It defaults to SQLite so the
app runs locally with zero setup (see the project's "local/simulated
alternative" philosophy), but because everything goes through SQLAlchemy,
swapping DATABASE_URL in .env to a managed Postgres instance (Supabase,
Neon, AWS RDS, Cloud SQL) is enough to move this to a real cloud database
with no code changes.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """Create all tables. Called once on app startup."""
    from backend.models import user, diet_plan, user_file  # noqa: F401  (ensure models are registered)
    Base.metadata.create_all(bind=engine)
