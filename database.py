"""
Database connection and initialization.
SQLAlchemy ORM setup with SQLite.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# SQLite database URL (file-based)
DATABASE_URL = "sqlite:///./task_manager.db"

# Create engine with connection pool
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    poolclass=StaticPool,  # Simple pool for SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_database_connection() -> dict[str, str]:
    """
    Validate database connection and return status.
    
    Returns:
        dict with connection status and details
    """
    try:
        with engine.connect() as connection:
            # Test the connection
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        return {
            "status": "✓ Connected",
            "database": "SQLite",
            "path": DATABASE_URL,
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "✗ Failed",
            "database": "SQLite",
            "path": DATABASE_URL,
            "error": str(e)
        }


def init_database():
    """Initialize database tables."""
    try:
        from models import Base
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables initialized")
    except Exception as e:
        print(f"Error initializing database: {e}")
