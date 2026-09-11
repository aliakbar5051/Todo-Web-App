### Screenshots 
<img width="2137" height="1703" alt="Screenshot 2026-09-09 214152" src="https://github.com/user-attachments/assets/570f27a6-552f-43f4-b221-96f75ae249fe" />
<img width="1955" height="1444" alt="Screenshot 2026-09-09 214202" src="https://github.com/user-attachments/assets/f4f7a878-8592-4c1e-9ebb-008ddd7d9fea" />
<img width="1955" height="1314" alt="Screenshot 2026-09-09 214209" src="https://github.com/user-attachments/assets/23fe0f3a-f057-4c99-9157-11de5094aecc" />
<img width="2052" height="1107" alt="Screenshot 2026-09-09 214223" src="https://github.com/user-attachments/assets/8634608e-1088-45f5-90b2-28bf7e39b387" />

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
