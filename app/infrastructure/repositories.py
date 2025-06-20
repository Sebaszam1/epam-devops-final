import datetime
from domain.entities import User, HealthCheck, HealthStatus
from domain.repositories import UserRepository, HealthRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        # Para este ejemplo simple, tenemos algunos usuarios predefinidos
        self._users = {"sebas": User(username="sebas")}
    
    def get_user_by_username(self, username: str) -> User:
        # Si el usuario existe en nuestro "almacén", lo retornamos
        if username in self._users:
            return self._users[username]
        else:
            # Si no existe, creamos y retornamos el usuario dinámicamente
            # En un caso real, aquí podrías lanzar una excepción de "Usuario no encontrado"
            new_user = User(username=username)
            self._users[username] = new_user  # Lo guardamos para futuras consultas
            return new_user


class InMemoryHealthRepository(HealthRepository):
    def get_health_status(self) -> HealthCheck:
        return HealthCheck(
            status=HealthStatus.HEALTHY,
            timestamp=datetime.datetime.now().isoformat()
        ) 