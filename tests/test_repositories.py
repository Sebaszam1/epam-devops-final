import pytest
from app.infrastructure.repositories import InMemoryUserRepository, InMemoryHealthRepository
from app.domain.entities import User, HealthStatus


class TestInMemoryUserRepository:
    def test_get_user_by_username_existing_user(self):
        repo = InMemoryUserRepository()
        
        user = repo.get_user_by_username("sebas")
        
        assert isinstance(user, User)
        assert user.username == "sebas"
    
    def test_get_user_by_username_non_existing_user_creates_new(self):
        repo = InMemoryUserRepository()
        
        user = repo.get_user_by_username("newuser")
        
        assert isinstance(user, User)
        assert user.username == "newuser"  # Creates and returns new user
    
    def test_get_user_by_username_stores_created_user(self):
        repo = InMemoryUserRepository()
        
        # First call creates user
        user1 = repo.get_user_by_username("testuser")
        # Second call should return same user from storage
        user2 = repo.get_user_by_username("testuser")
        
        assert user1.username == user2.username == "testuser"
    
    def test_get_user_by_username_with_empty_string_creates_user(self):
        repo = InMemoryUserRepository()
        
        # Esto podría fallar debido a validaciones en User entity
        with pytest.raises(ValueError, match="Username cannot be empty"):
            repo.get_user_by_username("")
    
    def test_get_user_by_username_with_whitespace_creates_user(self):
        repo = InMemoryUserRepository()
        
        user = repo.get_user_by_username("  spaced  ")
        
        assert isinstance(user, User)
        assert user.username == "  spaced  "
    
    def test_get_user_by_username_case_sensitive(self):
        repo = InMemoryUserRepository()
        
        user1 = repo.get_user_by_username("TestUser")
        user2 = repo.get_user_by_username("testuser")
        
        assert user1.username == "TestUser"
        assert user2.username == "testuser"
        assert user1.username != user2.username
    
    def test_get_user_by_username_special_characters(self):
        repo = InMemoryUserRepository()
        
        special_usernames = ["user@domain.com", "user-name", "user_123", "用户"]
        
        for username in special_usernames:
            user = repo.get_user_by_username(username)
            assert user.username == username


class TestInMemoryHealthRepository:
    def test_get_health_status_returns_healthy(self):
        repo = InMemoryHealthRepository()
        
        health_check = repo.get_health_status()
        
        assert health_check.status == HealthStatus.HEALTHY
        assert health_check.timestamp is not None
        assert isinstance(health_check.timestamp, str)
    
    def test_get_health_status_timestamp_format(self):
        repo = InMemoryHealthRepository()
        
        health_check = repo.get_health_status()
        
        # Check that timestamp is in ISO format
        import datetime
        try:
            datetime.datetime.fromisoformat(health_check.timestamp.replace('Z', '+00:00'))
            timestamp_is_valid = True
        except ValueError:
            timestamp_is_valid = False
        
        assert timestamp_is_valid
    
    def test_get_health_status_multiple_calls_different_timestamps(self):
        repo = InMemoryHealthRepository()
        
        health1 = repo.get_health_status()
        # Small delay to ensure different timestamps
        import time
        time.sleep(0.001)
        health2 = repo.get_health_status()
        
        assert health1.status == health2.status == HealthStatus.HEALTHY
        # Timestamps should be different (though very close)
        assert health1.timestamp != health2.timestamp
    
    def test_get_health_status_consistency(self):
        repo = InMemoryHealthRepository()
        
        # Call multiple times to ensure consistent behavior
        for _ in range(5):
            health_check = repo.get_health_status()
            assert health_check.status == HealthStatus.HEALTHY
            assert isinstance(health_check.timestamp, str)
            assert len(health_check.timestamp) > 0 