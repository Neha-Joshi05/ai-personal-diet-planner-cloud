import os
import sys
from pathlib import Path

# Make the project root importable (so `import backend...`, `import ai_engine...` work)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Point the app at a throwaway test database BEFORE importing it.
TEST_DB = ROOT / "test_diet_planner.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["UPLOAD_DIR"] = str(ROOT / "test_storage")
os.environ["SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.database import init_db


@pytest.fixture(scope="session", autouse=True)
def _cleanup():
    # TestClient only runs FastAPI's startup event inside a `with` block,
    # so create the tables explicitly here to keep the fixtures simple.
    init_db()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers(client):
    """Registers a fresh demo user (unique email per test) and returns an auth header."""
    import uuid
    email = f"demo-{uuid.uuid4().hex[:8]}@example.com"
    res = client.post("/register", json={
        "name": "Demo User", "email": email, "password": "password123",
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
