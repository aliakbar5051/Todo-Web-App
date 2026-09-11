from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from models.todo import Todo
from schemas.todo import TodoCreate, TodoUpdate


def list_todos(db: Session) -> list[Todo]:
    """Return every todo, newest first."""
    stmt = select(Todo).order_by(Todo.created_at.desc(), Todo.id.desc())
    return list(db.scalars(stmt))


def get_todo(db: Session, todo_id: int) -> Todo:
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def create_todo(db: Session, data: TodoCreate) -> Todo:
    # One shared timestamp keeps created_at == updated_at on creation,
    # so the UI can tell "never edited" from "edited later".
    now = datetime.now(timezone.utc)
    todo = Todo(
        task=data.task,
        completed=data.completed,
        created_at=now,
        updated_at=now,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, todo_id: int, data: TodoUpdate) -> Todo:
    todo = get_todo(db, todo_id)

    # Only assign fields that actually change, so a no-op request does not
    # bump updated_at. Real changes refresh it via the column's onupdate.
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


def delete_todo(db: Session, todo_id: int) -> None:
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()


def delete_todos(db: Session, completed_only: bool = False) -> int:
    """Delete all todos, or only the completed ones. Returns the removed count."""
    stmt = delete(Todo)
    if completed_only:
        stmt = stmt.where(Todo.completed.is_(True))
    result = db.execute(stmt)
    db.commit()
    return result.rowcount
