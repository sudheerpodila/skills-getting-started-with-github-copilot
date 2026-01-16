import pytest
import json
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup", json={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]

    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup", json={"email": "test@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]

    # Test invalid activity
    response = client.post("/activities/Invalid Activity/signup", json={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Chess Club/signup", json={"email": "unregister@example.com"})

    # Test successful unregister
    response = client.request("DELETE", "/activities/Chess Club/unregister", json={"email": "unregister@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Chess Club" in data["message"]

    # Test unregister not signed up
    response = client.request("DELETE", "/activities/Chess Club/unregister", json={"email": "notsigned@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Student is not signed up" in data["detail"]

    # Test invalid activity
    response = client.request("DELETE", "/activities/Invalid Activity/unregister", json={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect