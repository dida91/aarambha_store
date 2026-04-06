# Aarambha Store

Production-ready single-seller eCommerce platform for Nepal.

## Architecture (ASCII)

```text
+---------------------+        +---------------------+
|  React + Vite UI    | <----> | Django + DRF API    |
|  (Aarambha Store)   |  HTTP  | (JWT + OpenAPI)     |
+---------------------+        +----------+----------+
                                           |
                             +-------------+-------------+
                             |                           |
                    +--------v--------+         +--------v--------+
                    | PostgreSQL 16   |         | Redis 7         |
                    | Orders/Catalog  |         | Cache/Queue     |
                    +-----------------+         +--------+--------+
                                                          |
                                                +---------v---------+
                                                | Celery Worker     |
                                                | Async jobs/tasks  |
                                                +-------------------+
```

## Folder structure

```text
.
├── backend
│   ├── accounts/
│   ├── catalog/
│   ├── promotions/
│   ├── shipping/
│   ├── cart/
│   ├── orders/
│   ├── common/
│   ├── config/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── test/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick Start (Docker)

### First-time setup and run (copy/paste)

```bash
cd /path/to/aarambha_store && docker compose up -d --build && docker compose ps && curl -i http://localhost:8000/api/catalog/products/ && curl -i http://localhost:8000/admin/
```

### Stop stack

```bash
docker compose down
```

### Local (without Docker)

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Validation commands

### Backend

```bash
cd backend
python -m ruff check .
python -m black --check .
python -m pytest -q
python manage.py makemigrations --check --dry-run
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
npm run test
```

## Core implemented features

- Aarambha Store branded backend/frontend
- Product CRUD + multiple Cloudinary images + validations
- Promo system with date/usage/per-user/public-user/min-cart constraints
- ShippingConfig single-active rule + zone-based delivery fee logic
- Atomic checkout with server-side Decimal math and stock lock flow
- Order lifecycle validation + rejection reason enforcement + status history timeline
- Customer order list/detail and seller order/status management endpoints
- Admin customizations for Product, PromoCode, ShippingConfig, and Order (actions + status history inline)
- Admin metrics endpoint for total/pending/rejected/today/month sales
- JWT auth endpoints, role-based permissions, pagination, filtering, throttles
- drf-spectacular OpenAPI endpoints
- Dockerized backend/frontend/postgres/redis/celery stack
- Backend + frontend critical-flow tests

## Known limitations / future improvements

- Celery tasks are scaffolded but no business async jobs are yet implemented.
- Payment gateway integration is not included yet.
- Frontend currently focuses on foundational flows; checkout UX and seller dashboard can be expanded.
- Additional end-to-end tests (Playwright/Cypress) can be added for cross-stack workflows.

## Troubleshooting

- **Blank frontend page / runtime crash**
  - Check browser console for runtime errors.
  - Verify backend API response shape at `http://localhost:8000/api/catalog/products/`.
  - Rebuild and restart: `docker compose up -d --build`.

- **Backend returns 500 on `/api/*`**
  - Ensure migrations are applied (compose now runs migrate before server start).
  - Check logs: `docker compose logs backend --tail=200`.

- **Backend root `/` returns Not Found**
  - This is expected; use `/admin/` or `/api/...` routes.

- **Admin styling/static missing**
  - Ensure `DEBUG=True` in local dev (compose sets this for backend).
  - Re-open `http://localhost:8000/admin/` after backend restart.

- **Docker socket permission denied**
  - Add your user to docker group and re-login:
    - `sudo usermod -aG docker $USER`
    - then log out/in (or restart shell session).

- **Port conflicts (5432, 6379, 8000, 5173)**
  - Override host ports in `docker-compose.yml` (left side of `host:container`).
  - Example: change `5432:5432` to `55432:5432` if local Postgres already uses 5432.
