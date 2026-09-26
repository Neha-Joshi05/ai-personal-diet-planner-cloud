# Architecture

## Data flow

```
User
 |
 v
React frontend (frontend/)
 |  fetch() with a JWT bearer token
 v
REST API -- FastAPI (backend/app.py, backend/routes/)
 |
 |-- Auth: backend/utils/security.py (bcrypt hashing, JWT issue/verify)
 |
 |-- Profile / Plans / Files routes
 |     |
 |     v
 |   backend/services/  (business logic, e.g. plan_service.py)
 |     |
 |     v
 |   ai_engine/diet_engine.py   -- Version A rule-based engine (always available)
 |                                  Version B optional external AI API, with
 |                                  automatic fallback to Version A on any failure
 |     |
 |     v
 |   cloud/database_service.py -- structured data (users, plans)
 |   cloud/storage_service.py  -- file bytes (exported plans)
 |     |
 |     v
 |   SQLite (local) / managed Postgres (cloud)      <-- swap via DATABASE_URL
 |   local disk (local) / S3 or Firebase Storage      <-- swap via storage_service.py
 v
Dashboard (React) renders the response
```

## Why two separate "cloud" services

- **Cloud database** (`cloud/database_service.py`) stores *structured* data: user
  profiles, and each generated plan's meals/macros as rows you can query,
  filter, and sort. This is the `DIET_PLANS` / `USERS` design from the spec.
- **Cloud object storage** (`cloud/storage_service.py`) stores *files*: the
  `.txt` export of a plan. Real cloud platforms split these into different
  services (e.g. Cloud SQL/Firestore vs. Cloud Storage/S3) because they scale
  and price differently -- structured rows vs. arbitrary blobs.

Both are implemented locally (SQLite + local disk) so the whole project runs
with zero paid accounts, but every call goes through these two files, so
moving to a real managed database or object store later is a change in one
file each, not a rewrite of the routes or frontend.

## Cloud computing concepts demonstrated

| Concept | Where it appears |
|---|---|
| Client-server architecture | React frontend calls the FastAPI backend over HTTP |
| REST API | `backend/routes/*.py` -- resource-oriented endpoints, standard HTTP verbs/status codes |
| Authentication / Authorization | JWT issued on login, verified on every protected route (`backend/utils/deps.py`) |
| Cloud database | `cloud/database_service.py`, swappable via `DATABASE_URL` |
| Cloud object storage | `cloud/storage_service.py`, swappable to S3/Firebase Storage |
| Environment variables / secrets management | `backend/config.py` reads everything from `.env`; nothing hardcoded |
| User isolation | Every query in `database_service.py` filters by the caller's `user_id` |
| Serverless-style separation | `ai_engine/` is a standalone module -- it could be deployed as its own function/service |
| Scalability | See "Scaling this project" below |
| SaaS / PaaS / IaaS | See README -- the deployed app is a SaaS product; hosting it on Render/Railway is PaaS; provisioning raw VMs on AWS EC2 would be IaaS |

## Scaling this project

- **10 users:** exactly what's here today -- SQLite + local storage is fine.
- **1,000 users:** move `DATABASE_URL` to a managed Postgres instance (Supabase/Neon/RDS)
  and `storage_service.py` to S3/Firebase Storage; run the backend behind a
  process manager (gunicorn + multiple uvicorn workers).
- **100,000+ users:** put the backend behind a load balancer with autoscaling
  instances, add a CDN for the built frontend, add caching (Redis) for
  frequently-read data like the food catalog, and move long-running work
  (e.g. a future ML-based recommender) onto a queue instead of the request path.
