from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas import ProfileOut, ProfileUpdate
from backend.utils.deps import get_db, get_current_user
from backend.models.user import User
from cloud import database_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("", response_model=ProfileOut)
def update_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = database_service.update_profile(db, current_user, payload.model_dump())
    return updated
