"""
Pydantic schemas -- these validate every request body and shape every
response, which is also what powers the automatic OpenAPI docs at /docs.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Profile ----------
class ProfileUpdate(BaseModel):
    age: int = Field(ge=10, le=100)
    sex: str  # "male" | "female"
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    activity_level: str  # sedentary | light | moderate | active
    dietary_preference: str  # veg | vegan | nonveg
    goal: str  # maintain | lose | gain


class ProfileOut(BaseModel):
    user_id: int
    name: str
    email: str
    age: Optional[int] = None
    sex: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    dietary_preference: Optional[str] = None
    goal: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Diet plans ----------
class PlanOut(BaseModel):
    plan_id: int
    goal: str
    dietary_preference: str
    breakfast: dict
    lunch: dict
    snack: dict
    dinner: dict
    nutrition_summary: dict
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Files ----------
class FileOut(BaseModel):
    file_id: int
    filename: str
    size_kb: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class PlanListOut(BaseModel):
    plans: List[PlanOut]
