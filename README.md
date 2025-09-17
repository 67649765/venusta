![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/venus-ta-starter/venusta/ci.yml?branch=main)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-informational)
![Vite React](https://img.shields.io/badge/Vite-React-green)

# VenusTA — AI Teaching Assistant

End-to-end loop for **Generate → Grade → Diagnose → Review → Practice**, with Dockerized stack (FastAPI + Postgres + React+Vite via Nginx).

**Highlights**
- RAG-based exam generation (editable difficulty & ratio)
- Multi-judge LLM grading with tolerance & fallback
- 50+ error patterns, student profiling & dashboard
- One-line Docker Compose, health checks & smoke tests

**Quick Links**
- Frontend: http://localhost
- API Health: http://localhost/api/health
- Swagger: http://localhost/api/docs

## Table of Contents

1. [Features](#1-features)
2. [Architecture](#2-architecture)
3. [Quick Start](#3-quick-start)
4. [API & Frontend URLs](#4-api--frontend-urls)
5. [Configuration](#5-configuration)
6. [Dev Workflow](#6-dev-workflow)
7. [Test & Smoke](#7-test--smoke)
8. [CI/CD](#8-cicd)
9. [Troubleshooting](#9-troubleshooting)
10. [Project Structure](#10-project-structure)

## 1. Features

- **Intelligent Exam Generation**: RAG-based question creation with configurable difficulty and question type ratios
- **AI Grading System**: Multi-judge LLM evaluation with tolerance settings and automatic fallback mechanisms
- **Diagnostic Analysis**: Recognition of 50+ error patterns and generation of student ability profiles
- **Personalized Review**: Targeted revision recommendations based on performance
- **Data Visualization**: Interactive dashboards for tracking learning metrics and progress
- **One-Click Deployment**: Seamless environment setup with Docker Compose
- **Comprehensive Testing**: Built-in smoke tests and full-loop validation scripts

## 2. Architecture

```mermaid
flowchart LR
  subgraph Browser
    UI[Frontend (React+Vite)]
  end

  subgraph Docker
    Nginx[Nginx /api reverse proxy]
    API[FastAPI Service]
    DB[(PostgreSQL + init.sql)]
  end

  UI -->|/api/*| Nginx -->|HTTP| API -->|SQL| DB
```

## 3. Quick Start

### Using Docker Compose

```bash
# 1) Copy environment variables
cp .env.example .env

# 2) Start services
 docker compose up -d --build

# 3) Verify installation
curl http://localhost/api/health
# or open http://localhost and http://localhost/api/docs
```

### Using PowerShell

```powershell
Start-Service com.docker.service
Copy-Item .env.example .env -Force
docker compose up -d --build
curl http://localhost/api/health -UseBasicParsing
```

### Using Batch Scripts (Windows)

Double-click these files to run:
- `start_and_test_project.bat` - Full project startup and verification
- `run_full_loop.bat` - Run complete API test flow (Generate → Grade → Diagnose → Review → Dashboard)

## 4. API & Frontend URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | [http://localhost](http://localhost) | Main application interface |
| API Health (Proxied) | [http://localhost/api/health](http://localhost/api/health) | API health check through Nginx |
| API Health (Direct) | [http://localhost:8000/health](http://localhost:8000/health) | Direct API health check |
| Swagger Documentation | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive API documentation |

## 5. Configuration

Configure your `.env` file with the following variables:

| Key | Example | Notes |
|-----|---------|-------|
| POSTGRES_DB | `venusta` | Database name |
| POSTGRES_USER | `venusta` | Database username |
| POSTGRES_PASSWORD | `venusta` | Database password |
| POSTGRES_HOST | `db` | Compose service name |
| POSTGRES_PORT | `5432` | Internal container port |
| OPENAI_API_KEY | *(optional)* | Can be left empty for local development |
| OPENAI_BASE_URL | `https://api.openai.com/v1` | Customizable API endpoint |
| EMBEDDING_MODEL | `text-embedding-3-large` | Example embedding model |
| GENERATION_MODEL | `gpt-4o` | Example generation model |
| SCORING_JUDGE_COUNT | `3` | Multi-judge evaluation count |
| SCORING_TOLERANCE | `1` | Score tolerance threshold |

## 6. Dev Workflow

### Frontend Development Optimization

The frontend automatically switches API access based on environment:

* **Local Development**: `npm run dev` directly connects to `http://localhost:8000` (reducing container restarts)
* **Production/Container**: Frontend `.env` sets `VITE_API_BASE=/api`, with Nginx stripping the prefix

**Implementation in `src/api.ts`**:

```ts
const dev = import.meta.env.DEV;
export const API_BASE =
  dev ? "http://localhost:8000" : (import.meta.env.VITE_API_BASE || "/api");
```

## 7. Test & Smoke

### Full Loop Test

```bash
# PowerShell
powershell -ExecutionPolicy Bypass -File .\tools\full_loop.ps1 -VerboseLog

# Or
python tools/smoke_test.py

# Or use the batch script
run_full_loop.bat
```

### CI Smoke Test

```bash
python tools/ci_smoke_test.py
```

**Test Coverage**:
1. Generate a test paper
2. Grade answers
3. Perform diagnostic analysis
4. Generate review materials
5. Retrieve dashboard metrics

**If tests fail**: Check container logs
```bash
docker compose logs api
docker compose logs frontend
docker compose logs db
```

## 8. CI/CD

### GitHub Actions Workflow

- **Triggers**: `push/pull_request` to `main` branch
- **Steps**:
  1. Checkout code
  2. Build with Docker Compose
  3. Healthcheck services
  4. Run smoke tests
  5. Collect logs on failure
- **Artifacts**: `docker logs` / `pytest` reports (when available)

**Example GitHub Actions Configuration**:

```yaml
# .github/workflows/ci.yml
- name: Smoke Test
  run: |
    pwsh -File tools/full_loop.ps1
```



## 9. Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| `http://localhost/api/health` returns 404 | Check `nginx.conf` `proxy_pass` for trailing slash | Add `/` to `proxy_pass http://api:8000/;` to strip prefix |
| API cannot connect to database | `docker compose logs api`, `db` | Verify `.env` `POSTGRES_*` settings; check if `init.sql` ran on first startup |
| Frontend CORS/path errors when calling API | Check `.env` `VITE_API_BASE` is `/api` | Use direct 8000 port for local development, proxy for production |
| Port conflicts | `netstat -ano` | Change compose mappings or free the ports |
| Edge browser triggers Bing search errors | Browser address bar behavior | Enter full URLs or use batch scripts; disable "Use Bing for searches" in Edge settings |

## Project Structure

```
services/
├── .env                  # Environment variables
├── .env.example          # Environment variables example
├── .github/workflows/ci.yml  # GitHub Actions CI configuration
├── api/                  # Backend API service
│   ├── Dockerfile        # API Docker configuration
│   ├── app/              # Backend application code
│   │   ├── main.py       # API entry point
│   │   ├── routers/      # API routes
│   │   ├── db.py         # Database connection
│   │   └── tests/        # Backend tests
│   └── scripts/          # Backend scripts
│       └── seed_questions.py # Question bank initialization script
├── db/                   # Database initialization scripts
├── docker-compose.yml    # Docker Compose configuration
├── run_full_loop.bat     # One-click API test script
├── start_and_test_project.bat # Project startup and test script
├── tools/                # Test and utility scripts
│   ├── ci_smoke_test.py  # CI environment smoke test
│   ├── full_loop.ps1     # Full test flow
│   └── smoke_test.py     # Smoke test
└── venusta-frontend/     # Frontend React application
    ├── .env              # Frontend environment variables
    ├── Dockerfile        # Frontend Docker configuration
    ├── nginx.conf        # Nginx configuration
    ├── package.json      # Frontend dependencies
    └── src/              # Frontend source code
        ├── App.tsx       # Main application component
        ├── api.ts        # API call encapsulation
        └── main.tsx      # Entry point
```

## Demo Preparation

For project demonstrations, we recommend preparing in advance:

1. **Initialize seed data**
   ```powershell
   python .\api\scripts\seed_questions.py
   ```

2. **Warm up the system with full test script**
   ```powershell
   .\run_full_loop.bat
   ```

3. **Check all service statuses**
   ```powershell
   docker compose ps
   ```

4. **Ensure stable network connection**
   Some external services might be restricted in certain regions.

## License

This project is licensed under the MIT License.

## Contact

For any questions or further assistance, please contact the project team.