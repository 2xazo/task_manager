"""
User management endpoints.
In-memory storage only (no database).
"""

from fastapi import APIRouter

from schemas.models import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

# In-memory storage for users
users_db: list[User] = []
_user_id_counter = 1


@router.post("", response_model=User)
def create_user(user: UserCreate) -> User:
    """Create a new user."""
    global _user_id_counter
    new_user = User(id=_user_id_counter, **user.model_dump())
    users_db.append(new_user)
    _user_id_counter += 1
    return new_user


@router.get("", response_model=list[User])
def list_users() -> list[User]:
    """List all users."""
    return users_db
