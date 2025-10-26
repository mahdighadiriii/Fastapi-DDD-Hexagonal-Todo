# 🚀 FastAPI DDD Hexagonal Architecture - Todo API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)

**A production-ready Todo API implementing Domain-Driven Design (DDD) and Hexagonal Architecture principles**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Testing](#-testing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Design Patterns](#-design-patterns)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

This project demonstrates a **production-grade** implementation of a Todo API using **FastAPI** with **Domain-Driven Design (DDD)** and **Hexagonal Architecture** (Ports & Adapters). It showcases best practices for building scalable, maintainable, and testable Python applications.

### Why This Architecture?

- **🎯 Domain-Centric**: Business logic isolated from infrastructure concerns
- **🔌 Pluggable**: Easy to swap implementations (database, message queue, etc.)
- **🧪 Testable**: High test coverage with isolated unit tests
- **📈 Scalable**: Clean separation enables horizontal scaling
- **🛡️ Maintainable**: Clear boundaries reduce coupling and technical debt

## ✨ Features

- ✅ **CQRS Pattern** - Separate read and write models
- ✅ **Event-Driven Architecture** - Domain events for loose coupling
- ✅ **Unit of Work Pattern** - Transactional consistency
- ✅ **Repository Pattern** - Data access abstraction
- ✅ **Value Objects** - Type-safe domain primitives
- ✅ **Domain Events** - Business event tracking
- ✅ **API Versioning** - Future-proof API design
- ✅ **Exception Handling** - Centralized error management
- ✅ **Docker Support** - Containerized deployment
- ✅ **Type Safety** - Full type hints with Python 3.12

## 🏗️ Architecture

This project follows the **Hexagonal Architecture** pattern, organizing code into three main layers:

```
┌─────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                  │
│  (FastAPI, SQLAlchemy, Event Handlers, External APIs)   │
└─────────────────────┬───────────────────────────────────┘
                      │ Adapters
┌─────────────────────┴───────────────────────────────────┐
│                    Application Layer                     │
│     (Use Cases, DTOs, Interfaces/Ports)                  │
└─────────────────────┬───────────────────────────────────┘
                      │ Use Cases
┌─────────────────────┴───────────────────────────────────┐
│                      Domain Layer                        │
│  (Entities, Value Objects, Domain Events, Repositories)  │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

**🎯 Domain Layer** (Core Business Logic)
- Entities and Aggregates
- Value Objects
- Domain Events
- Repository Interfaces
- Business Rules and Invariants

**⚙️ Application Layer** (Use Cases)
- Command Handlers (Write Operations)
- Query Handlers (Read Operations)
- DTOs (Data Transfer Objects)
- Port Interfaces (UnitOfWork, EventBus)

**🔌 Infrastructure Layer** (Technical Details)
- FastAPI REST endpoints
- SQLAlchemy ORM models
- Database repositories
- Event bus implementation
- Middleware and exception handlers

## 🛠️ Technology Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | Latest |
| **Python** | Programming language | 3.12+ |
| **PostgreSQL** | Database | Latest |
| **SQLAlchemy** | ORM | Latest |
| **Poetry** | Dependency management | Latest |
| **Docker** | Containerization | Latest |
| **Pydantic** | Data validation | v2.0+ |

## 📁 Project Structure

```
src/
├── domain/                    # Core business logic
│   ├── entities/              # Domain entities
│   │   └── todo.py           # Todo aggregate root
│   ├── value_objects/        # Immutable value types
│   │   ├── todo_id.py        # Unique identifier
│   │   ├── todo_status.py    # Status enum
│   │   └── priority.py       # Priority enum
│   ├── events/               # Domain events
│   │   ├── base.py           # Base event
│   │   └── todo_events.py    # Todo-specific events
│   ├── repositories/         # Repository interfaces
│   │   └── todo_repository.py
│   └── exceptions.py         # Domain exceptions
│
├── application/              # Use cases and DTOs
│   ├── use_cases/
│   │   ├── commands/         # Write operations (CQRS)
│   │   │   ├── create_todo.py
│   │   │   ├── update_todo.py
│   │   │   └── complete_todo.py
│   │   └── queries/          # Read operations (CQRS)
│   │       ├── get_todo.py
│   │       └── list_todos.py
│   ├── dto/                  # Data transfer objects
│   │   └── todo_dto.py
│   └── interfaces/           # Port interfaces
│       ├── unit_of_work.py
│       └── event_bus.py
│
├── infrastructure/           # External adapters
│   ├── api/                  # FastAPI layer
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── todos.py
│   │       ├── schemas.py
│   │       └── dependencies.py
│   ├── persistence/          # Database layer
│   │   └── sqlalchemy/
│   │       ├── models.py
│   │       ├── repositories.py
│   │       ├── read_repositories.py
│   │       ├── unit_of_work.py
│   │       └── database.py
│   └── events/               # Event handling
│       ├── event_bus.py
│       └── handlers.py
│
├── config/                   # Configuration
│   └── settings.py
│
└── main.py                   # Application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Poetry
- Docker & Docker Compose
- PostgreSQL (or use Docker)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahdighadiriii/Fastapi-DDD-Hexagonal-Todo.git
   cd Fastapi-DDD-Hexagonal-Todo
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Start PostgreSQL (using Docker)**
   ```bash
   cd postgres
   docker-compose up -d
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run migrations**
   ```bash
   poetry run alembic upgrade head
   ```

6. **Start the application**
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Requirements.txt

If you prefer pip over Poetry:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## ⚙️ Configuration

Configuration is managed through `src/config/settings.py` using Pydantic settings.

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Application
APP_NAME=Todo API
VERSION=1.0.0
DEBUG=true

# API
API_V1_PREFIX=/api/v1
```

## 📚 API Documentation

### Endpoints

#### Create Todo
```http
POST /api/v1/todos
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive README",
  "priority": "HIGH"
}
```

#### Get Todo
```http
GET /api/v1/todos/{todo_id}
```

#### List Todos
```http
GET /api/v1/todos?status=PENDING&priority=HIGH&skip=0&limit=10
```

#### Update Todo
```http
PUT /api/v1/todos/{todo_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "priority": "MEDIUM"
}
```

#### Complete Todo
```http
POST /api/v1/todos/{todo_id}/complete
```

#### Delete Todo
```http
DELETE /api/v1/todos/{todo_id}
```

### Response Examples

**Success Response (201 Created)**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete project documentation",
  "description": "Write comprehensive README",
  "status": "PENDING",
  "priority": "HIGH",
  "created_at": "2025-10-26T10:30:00Z",
  "updated_at": "2025-10-26T10:30:00Z",
  "completed_at": null
}
```

**Error Response (404 Not Found)**
```json
{
  "detail": "Todo not found"
}
```

## 🎨 Design Patterns

### 1. **CQRS (Command Query Responsibility Segregation)**
Separates read and write operations for optimal performance and clarity.

- **Commands**: `create_todo.py`, `update_todo.py`, `complete_todo.py`
- **Queries**: `get_todo.py`, `list_todos.py`

### 2. **Repository Pattern**
Abstracts data access logic from business logic.

```python
# Domain interface
class TodoRepository(ABC):
    @abstractmethod
    async def add(self, todo: Todo) -> None:
        pass
```

### 3. **Unit of Work Pattern**
Manages transactions and ensures consistency.

```python
async with uow:
    todo = await uow.todos.get(todo_id)
    todo.complete()
    await uow.commit()
```

### 4. **Domain Events**
Decouples business logic through events.

```python
class TodoCompletedEvent(DomainEvent):
    todo_id: TodoId
    completed_at: datetime
```

### 5. **Value Objects**
Encapsulates domain concepts with validation.

```python
@dataclass(frozen=True)
class TodoId:
    value: UUID
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/domain/test_entities.py
```

### Test Structure

```
tests/
├── domain/           # Domain layer tests
├── application/      # Use case tests
├── infrastructure/   # Infrastructure tests
└── conftest.py       # Shared fixtures
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t fastapi-ddd-todo .

# Run container
docker run -p 8000:8000 fastapi-ddd-todo
```

### Docker Compose (Full Stack)

```bash
docker-compose up -d
```

## 📊 Performance Considerations

- **Connection Pooling**: SQLAlchemy manages database connections efficiently
- **Async/Await**: Non-blocking I/O for better concurrency
- **Read Models**: Optimized queries for read operations (CQRS)
- **Caching**: Can be easily integrated at the infrastructure layer
- **Indexing**: Database indexes on frequently queried fields

## 🔒 Security Best Practices

- Input validation using Pydantic
- SQL injection prevention via SQLAlchemy ORM
- Environment-based configuration
- CORS middleware configuration
- Exception handling without information leakage

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for public APIs
- Include unit tests for new features
- Update documentation as needed

## 📖 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mahdi Ghadiri**

- GitHub: [@mahdighadiriii](https://github.com/mahdighadiriii)
- Project: [Fastapi-DDD-Hexagonal-Todo](https://github.com/mahdighadiriii/Fastapi-DDD-Hexagonal-Todo)

---

<div align="center">

**⭐ If you find this project helpful, please consider giving it a star!**

Made with mahdi❤️ using FastAPI and Domain-Driven Design

</div>