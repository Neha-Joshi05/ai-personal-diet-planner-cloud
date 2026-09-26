"""
Shared FastAPI dependencies.

get_current_user is the authorization boundary of the whole app: every
protected route depends on it, which is what guarantees "user isolation"
(one user cannot read or modify another user's data) required by the spec.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.user import User
from backend.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_error

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_error
    return user
