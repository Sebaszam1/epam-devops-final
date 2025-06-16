from typing import Dict, Any
from app.domain.entities import User, HealthCheck, HealthStatus
from app.domain.repositories import UserRepository, HealthRepository
import datetime


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def execute(self, username: str) -> Dict[str, Any]:
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        user = self._user_repository.get_user_by_username(username.strip())
        return {"user": user.username}


class HealthCheckUseCase:
    def __init__(self, health_repository: HealthRepository):
        self._health_repository = health_repository
    
    def execute(self) -> Dict[str, Any]:
        health_check = self._health_repository.get_health_status()
        return {
            "status": health_check.status.value,
            "timestamp": health_check.timestamp or datetime.datetime.now().isoformat()
        } 