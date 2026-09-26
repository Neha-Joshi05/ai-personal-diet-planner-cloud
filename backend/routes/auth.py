from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas import UserRegister, UserLogin, Token
from backend.utils.deps import get_db
from backend.utils.security import hash_password, verify_password, create_access_token
from cloud import database_service

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if database_service.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = database_service.create_user(
        db, name=payload.name, email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    token = create_access_token(subject=user.user_id)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = database_service.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=user.user_id)
    return Token(access_token=token)
