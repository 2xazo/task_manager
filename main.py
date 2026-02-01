"""
Task Management System REST API.
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from routers import tasks, users
from database import init_database, validate_database_connection

app = FastAPI(
    title="Task Management API",
    description="Modular REST API for managing users and tasks",
    version="1.0.0",
)

# CORS - allows browsers to load docs and call API from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(tasks.router)

# Serve static files (HTML, CSS, JS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_database()
    db_status = validate_database_connection()
    print(f"Database Status: {db_status['status']}")
    print(f"Message: {db_status['message']}")


@app.get("/", tags=["root"], include_in_schema=False)
def root():
    """Root endpoint - returns HTML file."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return {"message": "Welcome to the Task API"}


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Health check endpoint with database validation."""
    db_status = validate_database_connection()
    return {
        "status": "healthy",
        "database": db_status
    }
