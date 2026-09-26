"""USER_FILES table -- metadata for files saved via the cloud storage service."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from backend.database import Base


class UserFile(Base):
    __tablename__ = "user_files"

    file_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)

    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)  # where cloud/storage_service.py put the bytes
    size_kb = Column(String, nullable=True)

    uploaded_at = Column(DateTime, default=datetime.utcnow)
