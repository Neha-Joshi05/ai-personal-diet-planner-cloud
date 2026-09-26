"""
Cloud Object Storage service.

Cloud DATABASE (database_service.py) holds structured records. Cloud
OBJECT STORAGE (this file) holds file bytes -- exported plans, uploaded
images, etc. Keeping them as separate services mirrors how a real cloud
architecture splits Cloud SQL/Firestore from S3/Firebase Storage/GCS.

This implementation writes to the local filesystem so the project runs
with zero cloud credentials. To move to a real cloud provider, replace
the three functions below with calls to that provider's SDK (boto3 for
S3, the Firebase Admin SDK for Firebase Storage, etc.) -- nothing outside
this file needs to change.
"""
import os
import shutil
from pathlib import Path

from backend.config import settings

BASE_DIR = Path(settings.UPLOAD_DIR)


def _user_dir(user_id: int) -> Path:
    path = BASE_DIR / str(user_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_file(user_id: int, filename: str, file_obj) -> dict:
    """Persist an uploaded file and return its storage metadata."""
    dest = _user_dir(user_id) / filename
    with open(dest, "wb") as out:
        shutil.copyfileobj(file_obj, out)
    size_kb = f"{dest.stat().st_size / 1024:.1f} KB"
    return {"filename": filename, "storage_path": str(dest), "size_kb": size_kb}


def delete_file(storage_path: str) -> bool:
    try:
        os.remove(storage_path)
        return True
    except FileNotFoundError:
        return False


def list_user_files(user_id: int) -> list[str]:
    directory = _user_dir(user_id)
    return [f.name for f in directory.iterdir() if f.is_file()]
