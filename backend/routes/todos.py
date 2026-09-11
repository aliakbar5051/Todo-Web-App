from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from services import todo_service

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    """List all todos, newest first."""
    return todo_service.list_todos(db)


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo."""
    return todo_service.create_todo(db, payload)


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)
):
    """Update a todo's text and/or completion status.

    The server refreshes updated_at automatically; clients never send
    timestamps. created_at stays untouched.
    """
    return todo_service.update_todo(db, todo_id, payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a single todo."""
    todo_service.delete_todo(db, todo_id)


@router.delete("")
def delete_todos(
    completed_only: bool = Query(
        default=False,
        description="If true, only completed todos are removed instead of all of them.",
    ),
    db: Session = Depends(get_db),
):
    """Remove all todos, or only the completed ones."""
    deleted = todo_service.delete_todos(db, completed_only=completed_only)
    return {"deleted": deleted}
