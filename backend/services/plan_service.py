"""
Business logic for generating and persisting a diet plan. Kept separate
from routes/plans.py so the route stays a thin HTTP layer and this logic
is unit-testable on its own.
"""
from sqlalchemy.orm import Session

from ai_engine.diet_engine import compute_targets, generate_plan
from cloud import database_service


def generate_and_save_plan(db: Session, user) -> "DietPlan":
    if not all([user.age, user.sex, user.height_cm, user.weight_kg, user.activity_level]):
        raise ValueError("Complete your profile before generating a plan.")

    target = compute_targets(
        age=user.age, sex=user.sex, height_cm=user.height_cm,
        weight_kg=user.weight_kg, activity_level=user.activity_level, goal=user.goal,
    )
    result = generate_plan(user.dietary_preference, target)

    nutrition_summary = {"target": target, "totals": result["totals"], "source": result["source"]}

    return database_service.save_plan(
        db=db,
        user_id=user.user_id,
        goal=user.goal,
        dietary_preference=user.dietary_preference,
        meals=result["meals"],
        nutrition_summary=nutrition_summary,
    )
