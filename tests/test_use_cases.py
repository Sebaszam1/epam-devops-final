import pytest
from unittest.mock import Mock
from app.application.use_cases import GetUserUseCase, HealthCheckUseCase
from app.domain.entities import User, HealthCheck, HealthStatus
from app.domain.repositories import UserRepository, HealthRepository


class TestGetUserUseCase:
    def test_execute_returns_user_data(self):
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        mock_user = User(username="sebas")
        mock_repo.get_user_by_username.return_value = mock_user
        
        use_case = GetUserUseCase(mock_repo)
        
        # Act
        result = use_case.execute("sebas")
        
        # Assert
        assert result == {"user": "sebas"}
        mock_repo.get_user_by_username.assert_called_once_with("sebas")
    
    def test_execute_with_different_username(self):
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        mock_user = User(username="testuser")
        mock_repo.get_user_by_username.return_value = mock_user
        
        use_case = GetUserUseCase(mock_repo)
        
        # Act
        result = use_case.execute("testuser")
        
        # Assert
        assert result == {"user": "testuser"}
        mock_repo.get_user_by_username.assert_called_once_with("testuser")
    
    def test_execute_with_empty_username_raises_error(self):
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        use_case = GetUserUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Username cannot be empty"):
            use_case.execute("")
    
    def test_execute_with_whitespace_username_raises_error(self):
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        use_case = GetUserUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Username cannot be empty"):
            use_case.execute("   ")
    
    def test_execute_trims_whitespace_from_username(self):
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        mock_user = User(username="trimmed")
        mock_repo.get_user_by_username.return_value = mock_user
        
        use_case = GetUserUseCase(mock_repo)
        
        # Act
        result = use_case.execute("  trimmed  ")
        
        # Assert
        assert result == {"user": "trimmed"}
        mock_repo.get_user_by_username.assert_called_once_with("trimmed")


class TestHealthCheckUseCase:
    def test_execute_returns_health_status(self):
        # Arrange
        mock_repo = Mock(spec=HealthRepository)
        timestamp = "2023-01-01T00:00:00"
        mock_health = HealthCheck(status=HealthStatus.HEALTHY, timestamp=timestamp)
        mock_repo.get_health_status.return_value = mock_health
        
        use_case = HealthCheckUseCase(mock_repo)
        
        # Act
        result = use_case.execute()
        
        # Assert
        assert result["status"] == "healthy"
        assert result["timestamp"] == timestamp
        mock_repo.get_health_status.assert_called_once()
    
    def test_execute_returns_current_timestamp_when_none(self):
        # Arrange
        mock_repo = Mock(spec=HealthRepository)
        mock_health = HealthCheck(status=HealthStatus.HEALTHY, timestamp=None)
        mock_repo.get_health_status.return_value = mock_health
        
        use_case = HealthCheckUseCase(mock_repo)
        
        # Act
        result = use_case.execute()
        
        # Assert
        assert result["status"] == "healthy"
        assert "timestamp" in result
        assert result["timestamp"] is not None
        mock_repo.get_health_status.assert_called_once() 