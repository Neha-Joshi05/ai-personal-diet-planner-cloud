"""
AI Diet Recommendation Engine.

VERSION A (implemented, always available):
    A rule-based engine. It computes calorie/macro targets with the
    Mifflin-St Jeor equation, then selects meals from food_data.json that
    are scaled toward those targets. No external API or paid service
    required -- this is what keeps the project fully executable for free.

VERSION B (optional, documented):
    generate_plan_ai() shows where a call to an external AI API would go.
    If AI_API_KEY is not configured, or the call fails for any reason,
    the engine automatically falls back to Version A. This fallback
    pattern -- try the AI service, catch failures, fall back to rules --
    is the "AI fallback mechanism" required by the project spec.
"""
import json
import random
from pathlib import Path

from backend.config import settings

FOOD_DATA_PATH = Path(__file__).parent / "food_data.json"

with open(FOOD_DATA_PATH, "r", encoding="utf-8") as f:
    FOOD_DB = json.load(f)

PAL = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
GOAL_DELTA = {"lose": -0.15, "gain": 0.15, "maintain": 0.0}


def compute_targets(age: int, sex: str, height_cm: float, weight_kg: float,
                     activity_level: str, goal: str) -> dict:
    """Mifflin-St Jeor BMR -> activity-adjusted TDEE -> goal-adjusted calories -> macros."""
    sex_offset = 5 if sex == "male" else -161
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + sex_offset
    tdee = bmr * PAL.get(activity_level, 1.2)
    calories = round(tdee * (1 + GOAL_DELTA.get(goal, 0.0)))

    # Default macro split: 30% protein / 40% carbs / 30% fat
    macros = {
        "p": round(0.30 * calories / 4),
        "c": round(0.40 * calories / 4),
        "f": round(0.30 * calories / 9),
    }
    return {"bmr": round(bmr), "tdee": round(tdee), "cal": calories, "macros": macros}


def _pick_and_scale(meal_options: list, scale: float) -> dict:
    item = random.choice(meal_options)
    return {
        "name": item["name"],
        "kcal": round(item["kcal"] * scale),
        "p": round(item["p"] * scale),
        "c": round(item["c"] * scale),
        "f": round(item["f"] * scale),
    }


def generate_plan_rule_based(dietary_preference: str, target: dict) -> dict:
    """VERSION A -- always works offline, no external dependency."""
    db = FOOD_DB.get(dietary_preference, FOOD_DB["veg"])
    scale = max(0.75, min(1.3, target["cal"] / 2000))

    meals = {slot: _pick_and_scale(db[slot], scale) for slot in ("breakfast", "lunch", "snack", "dinner")}
    totals = {
        "cal": sum(m["kcal"] for m in meals.values()),
        "p": sum(m["p"] for m in meals.values()),
        "c": sum(m["c"] for m in meals.values()),
        "f": sum(m["f"] for m in meals.values()),
    }
    return {"meals": meals, "totals": totals, "source": "rule_based"}


def generate_plan_ai(dietary_preference: str, target: dict) -> dict:
    """
    VERSION B -- optional external AI API call.

    This function is intentionally a stub: wire in your provider of choice
    (OpenAI, Anthropic, a hosted model, etc.) using settings.AI_API_KEY.
    Never hardcode the key -- it is only ever read from the environment.
    Any failure here (missing key, network error, bad response) must raise,
    so generate_plan() below can catch it and fall back to Version A.
    """
    if not settings.AI_API_KEY:
        raise RuntimeError("AI_API_KEY not configured")
    # Example shape of what a real integration would do:
    #   prompt = build_prompt(dietary_preference, target)
    #   response = call_external_ai_api(prompt, api_key=settings.AI_API_KEY)
    #   return validate_and_parse(response)
    raise NotImplementedError("Plug in a real AI provider here if desired")


def generate_plan(dietary_preference: str, target: dict) -> dict:
    """Public entry point used by the backend: try AI, fall back to rules."""
    try:
        return generate_plan_ai(dietary_preference, target)
    except Exception:
        return generate_plan_rule_based(dietary_preference, target)
