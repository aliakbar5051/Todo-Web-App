<img width="2301" height="1482" alt="Screenshot 2026-09-15 191155" src="https://github.com/user-attachments/assets/09ae502d-e026-419a-a13d-7927f97d6463" />
<img width="2052" height="1188" alt="Screenshot 2026-09-15 191322" src="https://github.com/user-attachments/assets/92791873-5900-4202-a438-b6b0f513c84a" />
<img width="1914" height="1116" alt="Screenshot 2026-09-15 191207" src="https://github.com/user-attachments/assets/77109962-f55c-4abb-85e1-8dc233b8b729" />
<img width="1822" height="1590" alt="Screenshot 2026-09-11 214453" src="https://github.com/user-attachments/assets/723dd686-828f-4903-9465-8a0242dade65" />
<img width="2211" height="1176" alt="Screenshot 2026-09-11 214501" src="https://github.com/user-attachments/assets/a118a524-aa4d-48b6-94ba-36ddae395d82" />
<img width="2133" height="1226" alt="Screenshot 2026-09-11 214510" src="https://github.com/user-attachments/assets/f1729be7-360e-49a8-9faa-479cdd8ecbe4" />
<img width="3330" height="1917" alt="Screenshot 2026-09-11 214527" src="https://github.com/user-attachments/assets/7c89c33c-59be-40f7-9525-5df9eeafc97d" />
<img width="3746" height="351" alt="Screenshot 2026-09-11 215917" src="https://github.com/user-attachments/assets/ad4d0114-59e3-4fc2-9112-e2148770bfac" />


# Todo Web App

A full-stack todo application: a React + Vite frontend talking to a FastAPI
backend, with PostgreSQL as the database (SQLAlchemy ORM, Pydantic schemas).

## Features

- Add, edit and delete todos
- Inline editing with Save / Cancel (Edit icon on every todo)
- Mark todos as completed
- Search todos
- Filter by All / Completed / Pending
- Clear completed / remove all todos
- `created_at` and `updated_at` stored per todo in PostgreSQL and shown
  under each task ("Created: ... · Updated: ...")

## Project structure

```
todo-app/
├── frontend/            React + Vite application
│   └── src/
│       ├── api/         fetch client for the backend
│       ├── components/  UI components
│       ├── hooks/       useTodos (state + API calls)
│       └── utils/       date formatting helpers
└── backend/             FastAPI application
    ├── main.py          app entrypoint (run with uvicorn)
    ├── database.py      engine, session and get_db dependency
    ├── models/todo.py   SQLAlchemy model (todos table)
    ├── schemas/todo.py  Pydantic request/response schemas
    ├── routes/todos.py  API routes
    ├── services/        business logic
    └── requirements.txt
```

## Database

Create a role and database once (adjust names/passwords as you like):

```sql
CREATE ROLE todo_app LOGIN PASSWORD 'your-password';
CREATE DATABASE todo_db OWNER todo_app;
```

The `todos` table is created automatically on backend startup:

| column      | type                   | notes                                    |
|-------------|------------------------|------------------------------------------|
| id          | integer (PK)           |                                          |
| task        | character varying(500) |                                          |
| completed   | boolean                | default false                            |
| created_at  | timestamptz            | set once on insert, never changed        |
| updated_at  | timestamptz            | refreshed automatically on every update  |

## Quick Start (One-Click)

- Run `start-all.bat` from the root directory to launch both backend and frontend servers in separate windows.
- Or run `start-backend.bat` to launch just the FastAPI backend server.

## Backend setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env   # then edit DATABASE_URL
```

To run the backend server:

```powershell
# From root directory:
.\start-backend.bat
# Or using the virtual environment:
.\backend\venv\Scripts\python.exe backend\main.py

# Or from backend directory:
cd backend
.\venv\Scripts\python.exe main.py
```

The API runs at http://127.0.0.1:8000 (interactive docs at http://127.0.0.1:8000/docs).


## Frontend setup

```powershell
cd frontend
npm install
npm run dev
```

The dev server runs at http://localhost:5173 and proxies `/api/*` to the
backend (see `vite.config.js`).

## API

| Method | Endpoint              | Description                              |
|--------|-----------------------|------------------------------------------|
| GET    | /api/todos            | List all todos (newest first)            |
| POST   | /api/todos            | Create a todo `{task, completed}`        |
| PUT    | /api/todos/{id}       | Update text and/or completion status     |
| DELETE | /api/todos/{id}       | Delete a single todo                     |
| DELETE | /api/todos            | Delete all todos (`?completed_only=true` keeps pending) |

Notes:

- Clients never send timestamps. `updated_at` is refreshed by the server on
  every real change (a no-op update does not bump it), and `created_at`
  never changes after creation.
- Task text is validated (1-500 chars, not blank); invalid payloads get a
  422, unknown ids a 404.
