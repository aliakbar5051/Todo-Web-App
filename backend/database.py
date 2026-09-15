import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        f"DATABASE_URL is not set. Expected .env file at '{ENV_FILE}'. "
        "Copy backend/.env.example to backend/.env and adjust the connection string."
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Provide a request-scoped session that is always closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create tables and execute migrations if needed."""
    # Import models so Base has all metadata registered
    import models.user  # noqa: F401
    import models.todo  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Check if todos table has user_id column
    inspector = inspect(engine)
    if "todos" in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns("todos")]
        if "user_id" not in columns:
            print("[MIGRATION] Adding user_id column to todos table...")
            with engine.begin() as conn:
                # Remove unowned legacy sample todos if any exist without user_id
                conn.execute(text("TRUNCATE TABLE todos RESTART IDENTITY CASCADE;"))
                # Add user_id with foreign key constraint to users(id)
                conn.execute(text(
                    "ALTER TABLE todos ADD COLUMN user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE;"
                ))
                conn.execute(text(
                    "CREATE INDEX IF NOT EXISTS ix_todos_user_id ON todos (user_id);"
                ))
            print("[MIGRATION] Successfully added user_id column and foreign key constraint.")
