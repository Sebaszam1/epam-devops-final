from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.application.use_cases import GetUserUseCase, HealthCheckUseCase
from app.infrastructure.repositories import InMemoryUserRepository, InMemoryHealthRepository


def get_user_repository():
    return InMemoryUserRepository()


def get_health_repository():
    return InMemoryHealthRepository()


def get_user_use_case(repo=Depends(get_user_repository)):
    return GetUserUseCase(repo)


def get_health_use_case(repo=Depends(get_health_repository)):
    return HealthCheckUseCase(repo)


router = APIRouter()


@router.get("/health", response_model=Dict[str, Any])
async def health_check(use_case: HealthCheckUseCase = Depends(get_health_use_case)):
    """
    Endpoint de healthcheck que retorna el estado de la aplicación
    """
    return use_case.execute()


@router.get("/user/{username}", response_model=Dict[str, str])
async def get_user(username: str, use_case: GetUserUseCase = Depends(get_user_use_case)):
    """
    Endpoint que retorna información del usuario basado en el username proporcionado
    """
    return use_case.execute(username) 