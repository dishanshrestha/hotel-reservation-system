# Hotel Reservation System (Python Backend)

This repository has been migrated from PHP/Laravel to a Python backend.

- Backend API: `backend/` (FastAPI + SQLAlchemy + JWT auth)
- Frontend files: `frontend/`
- SQL dump: `hotel.sql`

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Uvicorn
- SQLite by default (configurable via `DATABASE_URL`)

## Highlights

- Admin panel available at `frontend/public/admin/login.html`
- Admin dashboard supports:
	- room CRUD
	- gallery CRUD
	- bookings status updates
	- users list
- Image input supports both:
	- file upload (`image_file`)
	- image URL (`image_url`)
- Uploaded images are stored in `backend/media/` and served from `/media/*`

## Project Structure

- `backend/app.py`: API routes and business logic
- `backend/models.py`: SQLAlchemy models
- `backend/auth.py`: password hashing and JWT helpers
- `backend/database.py`: DB engine and session management
- `backend/requirements.txt`: Python dependencies
- `frontend/`: frontend assets and tooling

## Backend Setup

From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Run Backend

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

API base URL:

- `http://localhost:8000`

Health check:

- `GET /api/health`

## Environment Variables

Supported backend environment variables:

- `DATABASE_URL` (default: `sqlite:///backend/hotel.db`)
- `JWT_SECRET_KEY` (default fallback exists, set a secure value for production)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `1440`)
- `CORS_ORIGINS` (default: `*`, comma-separated list supported)

Example:

```bash
export DATABASE_URL="sqlite:///$(pwd)/backend/hotel.db"
export JWT_SECRET_KEY="replace-with-a-secure-random-secret"
export CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
```

## Frontend

Frontend source/static assets are in `frontend/`.
Vite is configured with `frontend/public` as the app root.

If you want to run frontend tooling:

```bash
cd frontend
npm install
npm run dev
```

## Notes About Migration

- Legacy PHP files were removed.
- Database table names used by the Python backend are aligned with the previous schema (`users`, `rooms`, `bookings`, `gallaries`, `contacts`, `room_ratings`).
- Uploaded files from API endpoints are stored under `backend/media/`.

## Admin Panel Usage

1. Start backend API:

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. Start frontend dev server:

```bash
cd frontend
npm install
npm run dev
```

3. Open admin login:

- `http://localhost:5173/admin/login.html`

4. Login using an account whose `usertype` is `admin`.

If you do not have an admin user yet, create one:

```bash
cd backend
python seed_admin.py --email admin@example.com --password StrongPass123! --name "Hotel Admin"
```
