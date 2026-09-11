from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

TASK_MAX_LENGTH = 500


class TodoCreate(BaseModel):
    """Payload for POST /api/todos."""

    task: str = Field(min_length=1, max_length=TASK_MAX_LENGTH)
    completed: bool = False

    @field_validator("task")
    @classmethod
    def task_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("task cannot be empty or only whitespace")
        return value


class TodoUpdate(BaseModel):
    """Payload for PUT /api/todos/{id}.

    Both fields are optional so text and completion status can be updated
    independently, but at least one must be provided.
    """

    task: str | None = Field(default=None, min_length=1, max_length=TASK_MAX_LENGTH)
    completed: bool | None = None

    @field_validator("task")
    @classmethod
    def task_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("task cannot be empty or only whitespace")
        return value

    @model_validator(mode="after")
    def at_least_one_field(self) -> "TodoUpdate":
        if self.task is None and self.completed is None:
            raise ValueError("provide at least one of 'task' or 'completed'")
        return self


class TodoResponse(BaseModel):
    """Todo as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    task: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def normalize_to_utc(cls, value: datetime) -> datetime:
        # PostgreSQL hands timestamps back in the server's timezone;
        # serialize a single consistent UTC form instead.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
