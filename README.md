# SafetyShield OG — HSE Management Platform

Oil & gas HSE (Health, Safety & Environment) management platform for incident tracking, permit to work (PTW), safety observations, and real-time HSE monitoring.

## Features

- **Incident Tracking** — Report and manage HSE incidents (near miss, first aid, medical treatment, lost time, fatality, environmental, fire, explosion)
- **Permit to Work (PTW)** — Create, approve, reject, and track work permits (hot work, cold work, confined space, height, electrical, excavation)
- **Safety Observations** — Log unsafe acts, unsafe conditions, and positive observations
- **Root Cause Analysis** — Identify recurring root causes across incidents
- **Safety Scoring** — Automated 0–100 safety score based on incidents, observations, and permit compliance
- **Real-time HSE Feed** — WebSocket-powered live safety event feed
- **HSE Analysis Agent** — Trend analysis, permit risk assessment, and report generation

## Quick Start

```bash
docker compose up -d
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy (async), PostgreSQL, JWT, WebSockets
- **Frontend:** React 18, TypeScript, Zustand, Recharts, Vite
- **Infrastructure:** Docker, Docker Compose

## Architecture

```
├── backend/
│   ├── app/
│   │   ├── api/          # REST + WebSocket endpoints
│   │   ├── agents/       # HSE analysis agent
│   │   ├── core/         # Config, security, database
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── store/        # Zustand state
│   └── Dockerfile
└── docker-compose.yml
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Login |
| GET/POST | /api/incidents/ | List/Create incidents |
| GET | /api/incidents/stats | Incident statistics |
| GET | /api/incidents/trends | Trend analysis |
| GET/POST | /api/permits/ | List/Create permits |
| GET | /api/permits/stats | Permit statistics |
| POST | /api/permits/{id}/approve | Approve permit |
| POST | /api/permits/{id}/reject | Reject permit |
| GET/POST | /api/observations/ | List/Create observations |
| WS | /ws/hse | Real-time HSE feed |

## License

MIT
