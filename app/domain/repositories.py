from abc import ABC, abstractmethod
from .entities import User, HealthCheck


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        pass


class HealthRepository(ABC):
    @abstractmethod
    def get_health_status(self) -> HealthCheck:
        pass 