# Aplicación Python con DDD

Una aplicación simple desarrollada con Python, FastAPI y arquitectura Domain Driven Design (DDD).

## Estructura del Proyecto

```
app/
├── __init__.py
├── main.py                    # Punto de entrada de la aplicación
├── domain/                    # Capa de dominio
│   ├── __init__.py
│   ├── entities.py           # Entidades del dominio
│   └── repositories.py       # Interfaces de repositorios
├── application/               # Capa de aplicación
│   ├── __init__.py
│   └── use_cases.py          # Casos de uso
└── infrastructure/            # Capa de infraestructura
    ├── __init__.py
    ├── repositories.py       # Implementaciones de repositorios
    └── controllers.py        # Controladores FastAPI

tests/                         # Pruebas unitarias
├── __init__.py
├── test_domain.py            # Pruebas del dominio
├── test_use_cases.py         # Pruebas de casos de uso
├── test_repositories.py      # Pruebas de repositorios
└── test_api.py              # Pruebas de integración API
```

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

### Ejecutar la aplicación:
```bash
# Desde la raíz del proyecto
python -m app.main
```

La aplicación estará disponible en `http://localhost:8000`

### Documentación automática:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### 1. Healthcheck
- **URL:** `GET /api/v1/health`
- **Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-01T12:00:00.000000"
}
```

### 2. Usuario
- **URL:** `GET /api/v1/user/{username}`
- **Parámetros:** 
  - `username` (string): Nombre de usuario a retornar
- **Ejemplos:**
  - `GET /api/v1/user/sebas` → `{"user": "sebas"}`
  - `GET /api/v1/user/admin` → `{"user": "admin"}`
  - `GET /api/v1/user/test123` → `{"user": "test123"}`

### 3. Raíz
- **URL:** `GET /`
- **Respuesta:**
```json
{
  "message": "Bienvenido a la API con DDD"
}
```

## Pruebas

### Ejecutar todas las pruebas:
```bash
pytest
```

### Ejecutar pruebas con cobertura:
```bash
pytest --cov=app
```

### Ejecutar pruebas específicas:
```bash
# Pruebas del dominio
pytest tests/test_domain.py

# Pruebas de casos de uso
pytest tests/test_use_cases.py

# Pruebas de repositorios
pytest tests/test_repositories.py

# Pruebas de API
pytest tests/test_api.py
```

## Arquitectura DDD

### Capa de Dominio (`app/domain/`)
- **Entidades:** Objetos con identidad que encapsulan reglas de negocio
- **Repositorios:** Interfaces que definen contratos para persistencia

### Capa de Aplicación (`app/application/`)
- **Casos de Uso:** Orquestan la lógica de negocio y coordinan entre dominio e infraestructura

### Capa de Infraestructura (`app/infrastructure/`)
- **Repositorios:** Implementaciones concretas de los contratos del dominio
- **Controladores:** Endpoints HTTP que exponen la funcionalidad de la aplicación

## Principios DDD Aplicados

1. **Separación de responsabilidades:** Cada capa tiene una responsabilidad específica
2. **Inversión de dependencias:** Las capas superiores dependen de abstracciones, no de implementaciones
3. **Entidades inmutables:** Uso de `dataclass(frozen=True)` para garantizar inmutabilidad
4. **Repositorios como abstracción:** Interfaces definidas en el dominio, implementadas en infraestructura

## Desarrollo

### Agregar nuevas funcionalidades:
1. Crear entidades en `app/domain/entities.py`
2. Definir interfaces de repositorio en `app/domain/repositories.py`
3. Implementar casos de uso en `app/application/use_cases.py`
4. Crear implementaciones de repositorio en `app/infrastructure/repositories.py`
5. Agregar controladores en `app/infrastructure/controllers.py`
6. Escribir pruebas unitarias correspondientes 