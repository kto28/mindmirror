# MindMirror — 每日正向心理測驗平台

每日一測，更了解自己。透過輕鬆有趣的正向心理測驗，探索你的內在傾向、生活風格與成長方向。

**Live:** https://mindmirror.eddyto.com

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| Backend | FastAPI (Python), SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| AI | OpenAI GPT-4o (structured JSON output) |
| Deployment | Ubuntu Server, Nginx, systemd, Let's Encrypt |

## Project Structure

```
/mindmirror
├── frontend/          # Next.js 14 app
│   ├── src/app/       # App Router pages
│   ├── src/components/# UI components
│   └── src/lib/       # API client, utilities
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── core/      # Config, DB, security
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── services/  # Business logic (scoring, generation)
│   │   ├── routers/   # API routes
│   │   └── prompts/   # OpenAI prompt templates
│   ├── alembic/       # DB migrations
│   └── seed.py        # Demo data seeder
└── docs/              # Deployment & integration docs
```

## Local Development

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create database
createdb mindmirror

# Run migrations (auto-creates tables on first start)
uvicorn app.main:app --reload --port 8000

# Seed demo data
python seed.py
```

### Frontend Setup

```bash
cd frontend
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_URL if needed

npm install
npm run dev
```

Open http://localhost:3000

### API Docs

With backend running: http://localhost:8000/api/docs

## Environment Variables

### Backend (.env)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `ADMIN_PASSWORD` | Admin login password |
| `JWT_SECRET` | JWT signing secret |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | Model name (default: gpt-4o) |
| `CORS_ORIGINS` | Comma-separated allowed origins |
| `AUTOMATION_SECRET` | Secret for n8n webhook calls |

### Frontend (.env.local)

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend API URL |

## Seed Data

3 demo quizzes included:
1. 你的旅行人格是什麼？
2. 你的社交電量恢復模式
3. 你的金錢安全感風格

Each with 5-6 questions, 4 options per question, and 4 result profiles.

## Build

```bash
# Frontend
cd frontend && npm run build

# Backend runs directly with uvicorn
```

## Deployment

See [docs/DEPLOY_UBUNTU.md](docs/DEPLOY_UBUNTU.md) for full Ubuntu deployment guide.
