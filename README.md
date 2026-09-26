# NutriCloud — AI-Powered Personal Diet Planner with Cloud Storage

A cloud-backed diet planner: users complete a profile, get a personalized
meal plan from a rule-based AI engine, and can revisit every past plan from
a history dashboard. Built as a Cloud Computing course project.

## Overview

NutriCloud demonstrates a complete cloud application architecture — a REST
API backend, a cloud database, cloud object storage, authentication, and a
React dashboard — using free/local-simulated services so it runs with zero
paid accounts, while staying structured so any piece can be swapped for a
real managed cloud service later.

## Problem statement

People struggle to plan meals, track macros, and stay consistent, and doing
it well usually means paying for an app or spreadsheet-managing it by hand.
NutriCloud generates a plan from a short profile and keeps every plan
accessible from any device via a central account.

## Objectives

- Generate a personalized meal plan from user goals and preferences
- Persist plans and files per user, isolated from other users
- Demonstrate core cloud computing concepts with real, runnable code
- Stay free-tier/local-friendly so it is easy to run and grade

## Features

- Register / login / logout with JWT authentication
- Profile: age, sex, height, weight, activity level, dietary preference, goal
- AI-generated diet plan: breakfast, lunch, snack, dinner + nutrition summary
- Plan history with a calorie trend and delete support
- Cloud file export/download of any plan, with a files list and delete support
- Dashboard: welcome, current goal, latest plan, macro split, plan count,
  hydration tracker

## Cloud computing concepts

See [`docs/architecture.md`](docs/architecture.md) for the full data-flow
diagram and a concept-by-concept breakdown (cloud database, cloud storage,
REST API, authentication, user isolation, scalability, SaaS/PaaS/IaaS).

## Technology stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + Vite + Tailwind CSS | Fast dev loop, matches the dashboard design |
| Backend | FastAPI | Async-ready, automatic OpenAPI docs at `/docs`, strong typing via Pydantic |
| Database | SQLite locally, swappable to managed Postgres | Zero setup locally, one env var to go to a real cloud DB |
| Auth | JWT + bcrypt (via `python-jose` / `passlib`) | Real security, no paid auth provider required |
| Object storage | Local filesystem, swappable to S3 / Firebase Storage | Same reasoning as the database |
| AI engine | Rule-based (Mifflin-St Jeor + food catalog), with an optional external-API hook | Always works offline; documented upgrade path |

## AI recommendation engine

`ai_engine/diet_engine.py` computes BMR/TDEE with the Mifflin-St Jeor
equation, derives a calorie target from the user's goal, and selects meals
from `ai_engine/food_data.json` scaled toward that target (**Version A**,
always available, no external dependency). `generate_plan()` first tries an
optional external AI API (**Version B**, stubbed — wire in a real provider
via `AI_API_KEY`) and automatically falls back to Version A on any failure,
so the app never breaks if an external service is unavailable or unconfigured.

## Authentication

Passwords are hashed with bcrypt and never stored or logged in plain text.
Login issues a JWT containing the user's id; every protected route decodes
and verifies that token (`backend/utils/deps.py`) before touching any data,
which is also what enforces **user isolation** — the query layer always
filters by the caller's own `user_id`, so one account can never read or
modify another account's plans or files.

## Database design

See `backend/models/` for the SQLAlchemy models and `docs/architecture.md`
for the schema diagram. Three tables: `users`, `diet_plans` (foreign key to
`users`), `user_files` (foreign key to `users`).

## Cloud storage

Exporting a plan (from the Generate page) writes a `.txt` file through
`cloud/storage_service.py` and records its metadata through
`cloud/database_service.py` — the split mirrors how a real deployment would
separate object storage (S3 / Firebase Storage) from the database (Postgres
/ Firestore).

## REST API

All endpoints are documented live at `/docs` (Swagger UI) once the backend
is running. Summary:

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/register` | — | Create an account, returns a JWT |
| POST | `/login` | — | Log in, returns a JWT |
| GET | `/profile` | ✓ | Get the current user's profile |
| PUT | `/profile` | ✓ | Update the current user's profile |
| POST | `/generate-plan` | ✓ | Generate and save a new plan |
| GET | `/plans` | ✓ | List the current user's plan history |
| GET | `/plans/{id}` | ✓ | Get one plan |
| DELETE | `/plans/{id}` | ✓ | Delete one plan |
| POST | `/upload` | ✓ | Upload/export a file |
| GET | `/files` | ✓ | List the current user's files |
| DELETE | `/files/{id}` | ✓ | Delete a file |

## Folder structure

```
AI-Personal-Diet-Planner-Cloud/
├── frontend/          React + Vite dashboard
├── backend/           FastAPI app, routes, models, services, auth
├── ai_engine/         Rule-based diet recommendation engine + food data
├── cloud/             Database + object storage service abstractions
├── tests/             Pytest suite (12 tests, all passing)
├── sample_data/       seed.py — creates a demo user + plan for quick testing
├── docs/              architecture.md
├── screenshots/       drop your screenshots here (see checklist below)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation & local setup

**Backend** (from the project root):
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # edit if you want, defaults work as-is
uvicorn backend.app:app --reload
```
Backend runs at `http://localhost:8000` — visit `/docs` for the live API reference.

**Frontend** (in a second terminal):
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

**Optional — seed a demo account:**
```bash
python sample_data/seed.py
```
Creates `demo@nutricloud.app` / `password123` with a completed profile and one plan.

## Environment variables

See `.env.example`. Nothing is hardcoded — `SECRET_KEY`, `DATABASE_URL`,
`UPLOAD_DIR`, `CORS_ORIGINS`, and the optional `AI_API_KEY` are all read from
the environment (`backend/config.py`).

## Running the application

1. Start the backend (`uvicorn backend.app:app --reload`)
2. Start the frontend (`npm run dev` inside `frontend/`)
3. Open `http://localhost:5173`, register an account, complete your profile,
   generate a plan, check History and Cloud files.

## Cloud deployment

**Approach A — free-tier friendly:**
- Frontend: deploy `frontend/` to Vercel or Netlify (`npm run build`, publish `dist/`)
- Backend: deploy `backend/` to Render or Railway as a web service
  (`uvicorn backend.app:app --host 0.0.0.0 --port $PORT`)
- Database: swap `DATABASE_URL` to a free-tier Postgres instance (Supabase or Neon)
- Set all `.env.example` variables as environment variables in the hosting dashboard

**Approach B — AWS/Azure/GCP:**
- Frontend: S3 + CloudFront (or the Azure/GCP equivalents) for static hosting
- Backend: containerize with a `Dockerfile` (`uvicorn` as the entrypoint) and
  run on ECS/Cloud Run/App Service
- Database: RDS / Cloud SQL / Azure Database for Postgres
- Object storage: S3 / GCS / Azure Blob Storage in place of `cloud/storage_service.py`
- Secrets: AWS Secrets Manager / GCP Secret Manager instead of a plain `.env` file

**Local development vs. cloud deployment:** locally everything points at
SQLite and the local disk for zero setup; in the cloud, the same code points
at managed services purely through environment variables — no code changes.

## Testing

Run the suite from the project root:
```bash
pytest tests/ -v
```
12 tests covering registration, duplicate-email rejection, login (valid and
invalid), profile → generate → history flow, vegan-preference filtering,
user isolation (one account cannot read another's plan), plan deletion, and
file upload/list/delete. All 12 pass against this codebase.

## Security

- Passwords hashed with bcrypt, never stored or logged in plain text
- JWT-based authentication/authorization on every protected route
- User isolation enforced at the query layer, not just the UI
- No secrets or credentials in source code — everything via environment variables (`.env`, gitignored)
- CORS restricted to configured origins only

**Common mistakes this project avoids (and to watch for in general):**
hardcoding secrets, trusting client-supplied user IDs instead of the JWT's,
skipping the user-id filter on a query, and logging sensitive fields.

## Scalability

See "Scaling this project" in [`docs/architecture.md`](docs/architecture.md).

## Screenshots

Suggested captures for your submission (save into `screenshots/`):
`01-folder-structure.png`, `02-architecture-diagram.png`, `03-register-page.png`,
`04-login-page.png`, `05-profile-page.png`, `06-generate-plan.png`,
`07-dashboard.png`, `08-history-page.png`, `09-cloud-files-page.png`,
`10-api-docs.png`, `11-test-results.png`, `12-github-repo.png`.

## Results

A working, end-to-end cloud application: authenticated users generate and
revisit personalized diet plans, with structured data and files kept
separately and correctly isolated per user.

## Limitations

Educational/demo project: the AI engine is rule-based (Version A) by
default; nutrition output is a general wellness estimate, not medical or
clinical advice; storage defaults to local disk/SQLite rather than a live
managed cloud service.

## Future improvements

Real managed-cloud deployment, a wired-up external AI provider for Version
B, meal-history analytics, barcode/food-image logging, CI/CD, containerized
deployment, infrastructure as code.

## Learning outcomes

Building this project covers: REST API design, JWT authentication, ORM
modeling, the structured-data-vs-object-storage split in cloud
architectures, environment-variable-based configuration, fallback design
for external dependencies, and writing tests against a real API.

## Disclaimer

This project uses synthetic/demo data. Generated diet plans are general
educational/wellness examples, not medical or clinical nutrition advice.

## Author

Built by Neha as a Cloud Computing course project.
