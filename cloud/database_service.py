"""
Cloud Database service.

This module is the single place the rest of the app talks to for reading
and writing structured data (users, plans). Routing all data access
through here -- instead of scattering SQLAlchemy queries across route
files -- is what makes it possible to swap the underlying database
(SQLite locally -> managed Postgres/Firestore in the cloud) without
touching any route or business logic.
"""
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.diet_plan import DietPlan
from backend.models.user_file import UserFile


# ---------- Users ----------
def create_user(db: Session, name: str, email: str, hashed_password: str) -> User:
    user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def update_profile(db: Session, user: User, profile: dict) -> User:
    for field, value in profile.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


# ---------- Diet plans ----------
def save_plan(db: Session, user_id: int, goal: str, dietary_preference: str,
              meals: dict, nutrition_summary: dict) -> DietPlan:
    plan = DietPlan(
        user_id=user_id,
        goal=goal,
        dietary_preference=dietary_preference,
        breakfast=meals["breakfast"],
        lunch=meals["lunch"],
        snack=meals["snack"],
        dinner=meals["dinner"],
        nutrition_summary=nutrition_summary,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def list_plans(db: Session, user_id: int) -> list[DietPlan]:
    # Filtering by user_id here (not just at the route layer) is the
    # "user isolation" guarantee -- one user's query can never return
    # another user's rows.
    return (
        db.query(DietPlan)
        .filter(DietPlan.user_id == user_id)
        .order_by(DietPlan.created_at.desc())
        .all()
    )


def get_plan(db: Session, user_id: int, plan_id: int) -> DietPlan | None:
    return (
        db.query(DietPlan)
        .filter(DietPlan.user_id == user_id, DietPlan.plan_id == plan_id)
        .first()
    )


def delete_plan(db: Session, user_id: int, plan_id: int) -> bool:
    plan = get_plan(db, user_id, plan_id)
    if not plan:
        return False
    db.delete(plan)
    db.commit()
    return True


# ---------- Files ----------
def create_file_record(db: Session, user_id: int, filename: str, storage_path: str, size_kb: str) -> UserFile:
    record = UserFile(user_id=user_id, filename=filename, storage_path=storage_path, size_kb=size_kb)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_files(db: Session, user_id: int) -> list[UserFile]:
    return (
        db.query(UserFile)
        .filter(UserFile.user_id == user_id)
        .order_by(UserFile.uploaded_at.desc())
        .all()
    )


def get_file(db: Session, user_id: int, file_id: int) -> UserFile | None:
    return db.query(UserFile).filter(UserFile.user_id == user_id, UserFile.file_id == file_id).first()


def delete_file_record(db: Session, user_id: int, file_id: int) -> UserFile | None:
    record = get_file(db, user_id, file_id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record
