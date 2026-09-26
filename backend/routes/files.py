from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from backend.schemas import FileOut
from backend.utils.deps import get_db, get_current_user
from backend.models.user import User
from cloud import database_service, storage_service

router = APIRouter(tags=["files"])


@router.post("/upload", response_model=FileOut, status_code=201)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Object storage: write the actual bytes.
    meta = storage_service.save_file(current_user.user_id, file.filename, file.file)
    # 2. Cloud database: record the metadata so it shows up in "GET /files".
    record = database_service.create_file_record(
        db, user_id=current_user.user_id,
        filename=meta["filename"], storage_path=meta["storage_path"], size_kb=meta["size_kb"],
    )
    return record


@router.get("/files", response_model=list[FileOut])
def get_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return database_service.list_files(db, current_user.user_id)


@router.delete("/files/{file_id}", status_code=204)
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = database_service.delete_file_record(db, current_user.user_id, file_id)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    storage_service.delete_file(record.storage_path)
