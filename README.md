# FastAPI Backend Server Template

A production-ready FastAPI template with clean architecture separation.

## Directory Structure

```
app/
├── main.py              # Application entry point
├── core/
│   ├── config.py        # Settings from .env
│   └── security.py      # Password hashing utilities
├── db/
│   ├── base.py          # SQLAlchemy Base class
│   ├── session.py       # Database engine & session factory
│   └── init_db.py       # Database initialization
├── models/
│   └── user.py          # SQLAlchemy ORM models
├── schemas/
│   └── user.py          # Pydantic DTO schemas
├── api/
│   ├── deps.py          # Dependency injection (get_db)
│   └── v1/
│       ├── router.py    # Mount all v1 endpoints
│       └── endpoints/
│           └── users.py # User HTTP routes
└── services/
    └── user_service.py  # Business logic layer
```

## Setup

### 1. Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Setup Environment

```powershell
Copy-Item .env.example .env
```

### 4. Run Server

```powershell
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

### 5. API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Users

- `GET /api/v1/users` - List all users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Health

- `GET /` - Welcome message
- `GET /health` - Health check

## Database Migrations (Alembic)

```powershell
# Create migration
alembic revision -m "description" --autogenerate

# Apply migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

### Migration Guide (PostgreSQL)

Use this flow whenever you change model datatypes (example: UUID to String).

1. Update your SQLAlchemy models first.
2. Generate migration from model changes.
3. Apply migration.
4. Verify current revision.

```powershell
# 1) Generate migration from model changes
.\.venv\Scripts\python.exe -m alembic revision -m "update_column_types" --autogenerate

# 2) Apply migration
.\.venv\Scripts\python.exe -m alembic upgrade head

# 3) Verify current revision
.\.venv\Scripts\python.exe -m alembic current
```

If you need to rebuild the database from scratch (migrate fresh), use this.
Warning: This removes all data in the public schema.

```powershell
# Recreate schema (fresh reset)
$env:PYTHONPATH = (Get-Location).Path
$py = @'
from app.db.session import engine
with engine.begin() as conn:
    conn.exec_driver_sql("DROP SCHEMA IF EXISTS public CASCADE")
    conn.exec_driver_sql("CREATE SCHEMA public")
print("Recreated public schema.")
'@
$tmp = New-TemporaryFile
Set-Content -Path $tmp -Value $py
.\.venv\Scripts\python.exe $tmp
Remove-Item $tmp

# Run all migrations again
.\.venv\Scripts\python.exe -m alembic upgrade head

# Verify revision
.\.venv\Scripts\python.exe -m alembic current
```

Optional check for specific column datatypes:

```powershell
$env:PYTHONPATH = (Get-Location).Path
$py = @'
from app.db.session import engine
from sqlalchemy import text
with engine.connect() as conn:
    rows = conn.execute(text("select table_name, column_name, data_type from information_schema.columns where table_name in ('batch','biological_assets') and column_name='batch_id' order by table_name")).fetchall()
    print(rows)
'@
$tmp = New-TemporaryFile
Set-Content -Path $tmp -Value $py
.\.venv\Scripts\python.exe $tmp
Remove-Item $tmp
```

## Architecture Layers

1. **Controllers (api/v1/endpoints/)** - HTTP request handling
2. **Schemas (schemas/)** - Pydantic validation & serialization
3. **Services (services/)** - Business logic
4. **Models (models/)** - SQLAlchemy ORM definitions
5. **DB (db/)** - Database connection & session management
6. **Core (core/)** - Config & security utilities

## Environment Variables

```env
DATABASE_URL=sqlite:///./app.db    # Database connection string
API_V1_STR=/api/v1                 # API v1 prefix
PROJECT_NAME=FastAPI Server        # Project name
DEBUG=True                          # Debug mode
```
