"""
Task Management System REST API.
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

from routers import tasks, users

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


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint - API welcome message."""
    return {"message": "Welcome to the Task API"}
