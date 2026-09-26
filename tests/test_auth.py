def test_register_new_user(client):
    res = client.post("/register", json={
        "name": "Neha", "email": "neha@example.com", "password": "password123",
    })
    assert res.status_code == 201
    assert "access_token" in res.json()


def test_register_duplicate_email_rejected(client):
    payload = {"name": "Neha", "email": "dupe@example.com", "password": "password123"}
    client.post("/register", json=payload)
    res = client.post("/register", json=payload)
    assert res.status_code == 400


def test_login_with_valid_credentials(client):
    client.post("/register", json={
        "name": "Neha", "email": "valid@example.com", "password": "password123",
    })
    res = client.post("/login", json={"email": "valid@example.com", "password": "password123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_with_invalid_password_rejected(client):
    client.post("/register", json={
        "name": "Neha", "email": "invalid@example.com", "password": "password123",
    })
    res = client.post("/login", json={"email": "invalid@example.com", "password": "wrong-password"})
    assert res.status_code == 401


def test_dashboard_requires_authentication(client):
    res = client.get("/profile")
    assert res.status_code == 401
