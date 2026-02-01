"""
Task Management System REST API.
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

from routers import tasks, users
from database import init_database, validate_database_connection

app = FastAPI(
    title="Task Management API",
    description="Modular REST API for managing users and tasks",
    version="1.0.0",
    docs_url=None,  # Disable default - we serve custom /docs below (unpkg CDN)
    redoc_url="/redoc",
)

# CORS - allows browsers to load docs and call API from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
def swagger_ui():
    """Swagger UI using unpkg CDN (works when jsdelivr is blocked)."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={"syntaxHighlight.theme": "monokai", "tryItOutEnabled": True},
    )

# Include routers
app.include_router(users.router)
app.include_router(tasks.router)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_database()
    db_status = validate_database_connection()
    print(f"Database Status: {db_status['status']}")
    print(f"Message: {db_status['message']}")


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint - API welcome message."""
    return {"message": "Welcome to the Task API"}


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Health check endpoint with database validation."""
    db_status = validate_database_connection()
    return {
        "status": "healthy",
        "database": db_status
    }
