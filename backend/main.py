import os
import sys
from pathlib import Path

# Ensure backend directory is in sys.path so imports work regardless of CWD
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes.auth import router as auth_router
from routes.todos import router as todos_router

# Initialize database schema and migrations
try:
    init_db()
except Exception as exc:
    print("\n" + "=" * 70, file=sys.stderr)
    print("[WARNING] Could not initialize PostgreSQL database!", file=sys.stderr)
    print(f"Error details: {exc}", file=sys.stderr)
    print("Please make sure your PostgreSQL service is running and configured.", file=sys.stderr)
    print("Connection string is configured in backend/.env", file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)

app = FastAPI(
    title="Todo API",
    description="Secure backend for the Todo web application with JWT authentication.",
    version="2.0.0",
)

# Configure CORS for allowed origins
cors_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(auth_router)
app.include_router(todos_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Secure Todo API is running",
        "docs": "/docs",
        "health": "/api/health",
        "auth": "/api/auth",
        "todos": "/api/todos",
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
