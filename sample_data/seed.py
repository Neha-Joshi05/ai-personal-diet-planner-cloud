"""
Optional helper: populates the database with one demo user, a completed
profile, and a generated plan -- useful for taking screenshots or for a
quick sanity check without clicking through the UI by hand.

Run from the project root:
    python sample_data/seed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.database import SessionLocal, init_db
from backend.utils.security import hash_password
from cloud import database_service
from backend.services.plan_service import generate_and_save_plan

DEMO_EMAIL = "demo@nutricloud.app"


def main():
    init_db()
    db = SessionLocal()

    user = database_service.get_user_by_email(db, DEMO_EMAIL)
    if not user:
        user = database_service.create_user(
            db, name="Demo Student", email=DEMO_EMAIL, hashed_password=hash_password("password123"),
        )
        print(f"Created demo user: {DEMO_EMAIL} / password123")
    else:
        print(f"Demo user already exists: {DEMO_EMAIL}")

    user = database_service.update_profile(db, user, {
        "age": 21, "sex": "female", "height_cm": 165, "weight_kg": 58,
        "activity_level": "moderate", "dietary_preference": "veg", "goal": "maintain",
    })

    plan = generate_and_save_plan(db, user)
    print(f"Generated demo plan #{plan.plan_id}: {plan.nutrition_summary['totals']['cal']} kcal")

    db.close()


if __name__ == "__main__":
    main()
