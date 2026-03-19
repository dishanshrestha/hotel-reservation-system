# Hotel Reservation System

This project was migrated from PHP/Laravel to:

- Backend: FastAPI + SQLAlchemy + JWT (`backend/`)
- Frontend: static pages served by Vite (`frontend/public/`)
- Database: SQLite by default

## What Is Implemented

- Public hotel website (home, rooms, gallery, blog, contact)
- Room booking flow without user panel/login
- Homepage `Book Now` redirects to `room.html` with selected dates
- Admin login and dashboard for room/gallery/bookings/users management
- Image management with both file upload and image URL options
- Media files stored in `backend/media/` and served at `/media/*`
- Booking confirmation email support via SMTP env configuration
- Room recommendation and alternative date suggestion algorithms wired to booking UI

## Algorithms Added

### 1) Weighted Multi-Factor Room Recommendation

- Endpoint: `GET /api/recommendations/rooms`
- Parameters:
	- `start_date`, `end_date` (optional pair)
	- `room_type` (optional)
	- `max_budget` (optional)
	- `wifi` (optional: `yes/no/true/false`)
	- `top_k` (default `3`, max `10`)
- How it works:
	- Filters out unavailable rooms for the requested date range.
	- Computes a weighted score per room using:
		- average rating,
		- price fit (budget-aware),
		- room type match,
		- wifi preference fit.
	- Uses a top-K ranking strategy to return best matches.
- Frontend wiring:
	- `room.html` calls this endpoint when arrival/departure dates are present.
	- Top recommendations are shown above the room list with quick-select buttons.

### 2) Merged-Interval Gap Scan For Alternative Availability

- Endpoint: `GET /api/rooms/{room_id}/availability-suggestions`
- Parameters:
	- `start_date`, `end_date` (required)
	- `max_suggestions` (default `3`, max `10`)
- How it works:
	- Collects room bookings as date intervals.
	- Merges overlapping/adjacent intervals.
	- Scans future gaps to find the next valid windows for the same stay length.
- Booking conflict integration:
	- `POST /api/bookings` and `POST /api/bookings/{room_id}` now return HTTP `409` with alternative slots when a date conflict occurs.
	- The room booking UI renders these suggestions as one-click date options.

## Project Structure

- `backend/app.py`: FastAPI app, routes, booking flow, admin APIs
- `backend/main.py`: compatibility ASGI entrypoint (`main:app`)
- `backend/auth.py`: JWT and password utilities
- `backend/database.py`: DB engine/session setup
- `backend/models.py`: SQLAlchemy models
- `backend/seed_admin.py`: helper script to create/update admin user
- `frontend/public/`: site/admin HTML, CSS, JS assets
- `frontend/vite.config.js`: Vite config (`public` as root)

## Requirements

- Python 3.11+
- Node.js 18+
- npm

## Quick Start

Use two terminals: one for backend, one for frontend.

### 1) Backend Setup And Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Alternative startup (also supported):

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend base URL: `http://127.0.0.1:8000`

Health check: `GET http://127.0.0.1:8000/api/health`

### 2) Frontend Setup And Run

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend URL: `http://localhost:5173`

## Environment Files

This repo uses service-level env files.

- Backend env: `backend/.env`
- Frontend env: `frontend/.env`

### Backend Env (`backend/.env`)

Key variables:

- `DATABASE_URL` (default SQLite)
- `JWT_SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_SENDER`
- `SMTP_USE_TLS`

Notes:

- If `SMTP_HOST` is empty, booking still works but email confirmation is skipped.
- To enable booking emails, set valid SMTP credentials.

### Frontend Env (`frontend/.env`)

- `VITE_API_BASE_URL=http://127.0.0.1:8000`

Frontend pages read this value and call backend APIs using that base URL.

## Important Routes

- Public home: `http://localhost:5173/`
- Rooms page: `http://localhost:5173/room.html`
- Admin login: `http://localhost:5173/admin/login.html`
- Admin redirect alias: `http://localhost:5173/login.html`

## Admin Access

Create an admin user (if needed):

```bash
cd backend
source .venv/bin/activate
python seed_admin.py --email admin@example.com --password StrongPass123! --name "Hotel Admin"
```

Then login at `http://localhost:5173/admin/login.html`.

## Build Commands

Frontend production build:

```bash
cd frontend
npm run build
```

## Migration Notes

- Legacy PHP/Laravel app files were removed.
- Existing schema-compatible table names are preserved (`users`, `rooms`, `bookings`, `gallaries`, `contacts`, `room_ratings`).
