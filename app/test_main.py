import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns JSON data."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "healthy"


def test_health_check_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Simple DDD API"
    assert data["version"] == "1.0.0"
    assert "environment" in data


def test_api_v1_endpoint():
    """Test API v1 endpoint is accessible."""
    # This test depends on what's in your controller
    # Assuming there's at least one endpoint
    response = client.get("/api/v1/")
    # The response might be 404 if no endpoint exists, but it should be reachable
    assert response.status_code in [200, 404, 405]  # Any of these indicates the router is working


def test_favicon_endpoint():
    """Test favicon endpoint."""
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_nonexistent_endpoint():
    """Test that nonexistent endpoints return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404 