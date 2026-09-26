"""USERS table -- see docs/architecture.md for the full schema explanation."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary key. Every child table (DietPlan, UserFile) stores this as a
    # foreign key, which is how we guarantee "one user cannot read another
    # user's data" -- every query below is filtered by the caller's own id.
    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Profile fields (collected in Step 2 of the project spec)
    age = Column(Integer, nullable=True)
    sex = Column(String, nullable=True)            # "male" | "female"
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    activity_level = Column(String, nullable=True)  # sedentary | light | moderate | active
    dietary_preference = Column(String, nullable=True)  # veg | vegan | nonveg
    goal = Column(String, nullable=True)            # maintain | lose | gain

    created_at = Column(DateTime, default=datetime.utcnow)
