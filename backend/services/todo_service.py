from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from models.todo import Todo
from schemas.todo import TodoCreate, TodoUpdate


def list_todos(db: Session, user_id: int) -> list[Todo]:
    """Return every todo belonging to user_id, newest first."""
    stmt = (
        select(Todo)
        .where(Todo.user_id == user_id)
        .order_by(Todo.created_at.desc(), Todo.id.desc())
    )
    return list(db.scalars(stmt))


def get_user_todo(db: Session, todo_id: int, user_id: int) -> Todo:
    """Retrieve a single todo belonging to user_id.
    
    If the todo does not exist or belongs to another user, raises 404
    to prevent information disclosure / IDOR.
    """
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = db.scalar(stmt)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return todo


def create_todo(db: Session, user_id: int, data: TodoCreate) -> Todo:
    """Create a new todo strictly bound to the authenticated user."""
    now = datetime.now(timezone.utc)
    todo = Todo(
        user_id=user_id,
        task=data.task,
        completed=data.completed,
        created_at=now,
        updated_at=now,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, todo_id: int, user_id: int, data: TodoUpdate) -> Todo:
    """Update a todo's task or completed status after verifying ownership."""
    todo = get_user_todo(db, todo_id, user_id)

    changed = False
    if data.task is not None and data.task != todo.task:
        todo.task = data.task
        changed = True
    if data.completed is not None and data.completed != todo.completed:
        todo.completed = data.completed
        changed = True

    if changed:
        db.commit()
        db.refresh(todo)

    return todo


def delete_todo(db: Session, todo_id: int, user_id: int) -> None:
    """Delete a single todo belonging to user_id after verifying ownership."""
    todo = get_user_todo(db, todo_id, user_id)
    db.delete(todo)
    db.commit()


def delete_todos(db: Session, user_id: int, completed_only: bool = False) -> int:
    """Delete all todos or only completed todos belonging strictly to user_id."""
    stmt = delete(Todo).where(Todo.user_id == user_id)
    if completed_only:
        stmt = stmt.where(Todo.completed.is_(True))
    result = db.execute(stmt)
    db.commit()
    return result.rowcount
