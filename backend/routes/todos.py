from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from services import todo_service

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse], summary="List all todos for current user")
def read_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all todos belonging to the authenticated user, newest first."""
    return todo_service.list_todos(db, current_user.id)


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, summary="Create a new todo")
def create_todo(
    payload: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new todo owned by the authenticated user."""
    return todo_service.create_todo(db, current_user.id, payload)


@router.put("/{todo_id}", response_model=TodoResponse, summary="Update a todo")
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a todo's text and/or completion status.
    
    Verifies that the todo belongs to the authenticated user. If not, returns 404.
    """
    return todo_service.update_todo(db, todo_id, current_user.id, payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a single todo")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a single todo belonging to the authenticated user."""
    todo_service.delete_todo(db, todo_id, current_user.id)


@router.delete("", summary="Delete all or completed todos for current user")
def delete_todos(
    completed_only: bool = Query(
        default=False,
        description="If true, only completed todos are removed instead of all of them.",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove all todos, or only completed ones, strictly for the authenticated user."""
    deleted = todo_service.delete_todos(db, current_user.id, completed_only=completed_only)
    return {"deleted": deleted}
