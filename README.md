# Task Management System REST API

A modular FastAPI REST API for managing users and tasks with Pydantic v2 validation.

> **Repository:** [https://github.com/2xazo/task_manager](https://github.com/2xazo/task_manager)

## Project Structure

```
task_manager/
├── main.py              # FastAPI application entry point
├── routers/
│   ├── users.py         # User management endpoints
│   └── tasks.py         # Task management endpoints
└── schemas/
    └── models.py        # Pydantic models and validators
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Or with Python module:

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Endpoints

- `GET /` - Welcome message
- `POST /users` - Create a user
- `GET /users` - List all users
- `POST /tasks` - Create a task
- `GET /tasks` - List tasks (filter by `status`, `priority`, `assigned_to`)

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Validation Rules

- **Task title**: Must start with a capital letter
- **User role**: `admin` | `manager` | `member`
- **Task priority**: `low` | `medium` | `high`
- **Task status**: `todo` | `in_progress` | `done`
