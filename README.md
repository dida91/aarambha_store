# Aarambha Store

Production-ready single-seller eCommerce platform for Nepal built with Django/DRF and React/Vite.

## ASCII Architecture Diagram

```
+-----------------------+            +-------------------------+
| React + Vite (TS) UI  |  HTTPS     | Django + DRF API        |
| Aarambha Store Front  +----------->+ JWT, business rules     |
+-----------+-----------+            +-----+-------------+-----+
            |                                 |             |
            |                                 |             |
            |                           +-----v-----+ +-----v------+
            |                           | PostgreSQL| |   Redis    |
            |                           | orders,   | | Celery MQ  |
            |                           | catalog   | +------------+
            |                           +-----------+        |
            |                                                |
            |                                         +------v------+
            +---------------------------------------->+ Celery Worker|
                                                      +-------------+

Media uploads -> Cloudinary
API docs -> drf-spectacular (/api/docs/swagger/)
```

## Folder Structure

```
.
├── backend
│   ├── accounts
│   ├── cart
│   ├── catalog
│   ├── common
│   ├── config
│   ├── orders
│   ├── promotions
│   ├── shipping
│   ├── tests
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── manage.py
├── frontend
│   ├── src
│   │   ├── test
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   ├── auth.tsx
│   │   ├── pages.tsx
│   │   └── types.ts
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Setup / Run Instructions

### Local backend
1. `cd backend`
2. `python -m pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py createsuperuser` (optional)
5. `python manage.py runserver`

### Local frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Docker
1. `docker compose up --build`
2. Backend: `http://localhost:8000`
3. Frontend: `http://localhost:5173`
4. Swagger: `http://localhost:8000/api/docs/swagger/`

## Quality checks

### Backend
- `ruff check .`
- `black --check .`
- `pytest -q`

### Frontend
- `npm run lint`
- `npm run build`
- `npm run test`

## Known Limitations / Future Improvements

- Frontend is intentionally minimal and should be expanded into full production UI flows.
- Add refresh token persistence/rotation handling in browser storage strategy.
- Expand test coverage for promo edge cases, admin actions, and shipping fee matrix.
- Add async tasks for post-order notifications and analytics pipelines.
- Add stricter PostgreSQL-only partial index behavior verification in CI.
