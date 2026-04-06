# Aarambha Store Frontend

Production-ready React + TypeScript + Vite storefront aligned to the backend API envelope and route contracts.

## Stack
- React 19 + TypeScript + Vite
- Tailwind CSS
- React Router
- Axios
- Context API (Auth, Cart, Toast)

## Project Structure
- `src/app` app bootstrap, routing, providers, contexts
- `src/components/common` reusable UI and route guards
- `src/components/layout` layout shell components
- `src/features/*` feature service modules
- `src/lib` API client, endpoint config, utilities
- `src/hooks` shared hooks
- `src/types` API and domain types
- `src/pages` route-based pages
- `src/styles` design tokens

## Environment Variables
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Variables:
- `VITE_API_BASE_URL` (required): backend API base URL (example: `http://localhost:8000/api`)
- `VITE_API_WITH_CREDENTIALS` (optional): `true` or `false` for cookie-based auth compatibility

## Setup
```bash
npm install
```

## Run Dev Server
```bash
npm run dev
```

## Build
```bash
npm run build
```

## Validate
```bash
npm run lint
npm run test
npm run build
```

## Auth + API Notes
- API requests are centralized in `src/lib/api.ts`.
- Request interceptor attaches `Bearer <access>` token.
- Response interceptor normalizes envelope errors and retries once using `/accounts/refresh/`.
- Tokens are persisted in `localStorage` for session restoration.

## Routes
- `/` Home
- `/products` Products
- `/products/:id` ProductDetails
- `/cart` Cart (protected)
- `/checkout` Checkout (protected)
- `/login` Login
- `/register` Register
- `/profile` Profile (protected)
- `*` NotFound
