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

## Setup & run instructions

### Local backend

```bash
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Local frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker compose

```bash
docker compose up --build
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
