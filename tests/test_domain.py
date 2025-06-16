import pytest
from app.domain.entities import User, HealthCheck, HealthStatus


class TestUser:
    def test_create_user_with_valid_username(self):
        user = User(username="sebas")
        assert user.username == "sebas"
    
    def test_create_user_with_empty_username_raises_error(self):
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(username="")
    
    def test_create_user_with_none_username_raises_error(self):
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(username=None)
    
    def test_create_user_with_non_string_username_raises_error(self):
        with pytest.raises(ValueError, match="Username must be a string"):
            User(username=123)


class TestHealthCheck:
    def test_create_health_check_with_valid_status(self):
        health_check = HealthCheck(status=HealthStatus.HEALTHY)
        assert health_check.status == HealthStatus.HEALTHY
        assert health_check.timestamp is None
    
    def test_create_health_check_with_timestamp(self):
        timestamp = "2023-01-01T00:00:00"
        health_check = HealthCheck(status=HealthStatus.HEALTHY, timestamp=timestamp)
        assert health_check.status == HealthStatus.HEALTHY
        assert health_check.timestamp == timestamp
    
    def test_create_health_check_with_invalid_status_raises_error(self):
        with pytest.raises(ValueError, match="Status must be a HealthStatus enum"):
            HealthCheck(status="invalid")


class TestHealthStatus:
    def test_health_status_enum_values(self):
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.UNHEALTHY.value == "unhealthy" 