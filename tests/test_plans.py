PROFILE = {
    "age": 24, "sex": "female", "height_cm": 165, "weight_kg": 60,
    "activity_level": "moderate", "dietary_preference": "veg", "goal": "maintain",
}


def test_generate_plan_requires_profile_first(client, auth_headers):
    res = client.post("/generate-plan", headers=auth_headers)
    assert res.status_code == 400


def test_full_flow_profile_then_generate_then_history(client, auth_headers):
    # Save profile
    res = client.put("/profile", json=PROFILE, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["dietary_preference"] == "veg"

    # Generate a plan
    res = client.post("/generate-plan", headers=auth_headers)
    assert res.status_code == 201
    plan = res.json()
    assert plan["nutrition_summary"]["target"]["cal"] > 0
    for meal in ("breakfast", "lunch", "snack", "dinner"):
        assert "kcal" in plan[meal]

    # It shows up in history
    res = client.get("/plans", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Fetch it directly
    plan_id = plan["plan_id"]
    res = client.get(f"/plans/{plan_id}", headers=auth_headers)
    assert res.status_code == 200


def test_vegan_preference_excludes_animal_products(client, auth_headers):
    profile = {**PROFILE, "dietary_preference": "vegan"}
    client.put("/profile", json=profile, headers=auth_headers)
    res = client.post("/generate-plan", headers=auth_headers)
    plan = res.json()
    meal_names = " ".join(plan[m]["name"].lower() for m in ("breakfast", "lunch", "snack", "dinner"))
    assert "egg" not in meal_names and "paneer" not in meal_names and "fish" not in meal_names and "chicken" not in meal_names


def test_user_cannot_read_another_users_plan(client):
    # User A creates a plan
    client.post("/register", json={"name": "A", "email": "a@example.com", "password": "password123"})
    token_a = client.post("/login", json={"email": "a@example.com", "password": "password123"}).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    client.put("/profile", json=PROFILE, headers=headers_a)
    plan_id = client.post("/generate-plan", headers=headers_a).json()["plan_id"]

    # User B tries to read it
    client.post("/register", json={"name": "B", "email": "b@example.com", "password": "password123"})
    token_b = client.post("/login", json={"email": "b@example.com", "password": "password123"}).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    res = client.get(f"/plans/{plan_id}", headers=headers_b)
    assert res.status_code == 404


def test_delete_plan(client, auth_headers):
    client.put("/profile", json=PROFILE, headers=auth_headers)
    plan_id = client.post("/generate-plan", headers=auth_headers).json()["plan_id"]
    res = client.delete(f"/plans/{plan_id}", headers=auth_headers)
    assert res.status_code == 204
    assert client.get(f"/plans/{plan_id}", headers=auth_headers).status_code == 404
