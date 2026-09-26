"""DIET_PLANS table -- one row per generated plan, forming the plan history."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON

from backend.database import Base


class DietPlan(Base):
    __tablename__ = "diet_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)

    goal = Column(String, nullable=False)
    dietary_preference = Column(String, nullable=False)

    # Stored as JSON so the whole meal breakdown (breakfast/lunch/snack/dinner
    # + per-meal macros) is retrievable in one row without extra joins.
    breakfast = Column(JSON, nullable=False)
    lunch = Column(JSON, nullable=False)
    snack = Column(JSON, nullable=False)
    dinner = Column(JSON, nullable=False)

    nutrition_summary = Column(JSON, nullable=False)  # {target, totals}

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
