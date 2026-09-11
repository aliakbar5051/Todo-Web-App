import os
import sys
from pathlib import Path

# Ensure backend directory is in sys.path so imports work regardless of CWD
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models.todo  # noqa: F401 - ensure models are registered with Base metadata
from database import Base, engine
from routes.todos import router as todos_router

# Create the tables on startup. Timestamps are owned by the database layer
# and are never accepted from clients.
try:
    Base.metadata.create_all(bind=engine)
except Exception as exc:
    print("\n" + "=" * 70, file=sys.stderr)
    print("[WARNING] Could not connect to PostgreSQL database!", file=sys.stderr)
    print(f"Error details: {exc}", file=sys.stderr)
    print("Please make sure your PostgreSQL service is running and the database exists.", file=sys.stderr)
    print("Connection string is configured in backend/.env", file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)

app = FastAPI(
    title="Todo API",
    description="Backend for the Todo web app.",
    version="1.0.0",
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Todo API is running",
        "docs": "/docs",
        "health": "/api/health",
        "todos": "/api/todos",
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

