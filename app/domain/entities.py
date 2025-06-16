from dataclasses import dataclass
from typing import Optional
from enum import Enum


class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


@dataclass(frozen=True)
class User:
    username: str
    
    def __post_init__(self):
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not isinstance(self.username, str):
            raise ValueError("Username must be a string")


@dataclass(frozen=True)
class HealthCheck:
    status: HealthStatus
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        if not isinstance(self.status, HealthStatus):
            raise ValueError("Status must be a HealthStatus enum") 