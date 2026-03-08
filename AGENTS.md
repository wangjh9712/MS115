# AGENTS.md

This file provides context and guidelines for AI coding agents working in this repository.

## Project Overview

MediaSync115 is a full-stack media sync application that searches movies/TV shows via Nullbr API (TMDB-based), manages subscriptions, and integrates with 115 cloud storage for file management and offline downloads.

**Tech Stack:**
- Frontend: Vue 3 (Composition API) + Vite 5 + Element Plus + Pinia + Axios + SCSS
- Backend: FastAPI + SQLAlchemy 2.0 (async) + SQLite (aiosqlite) + Pydantic 2.0
- Deployment: Docker + Docker Compose + Nginx

---

## Build/Lint/Test Commands

### Frontend (in `frontend/` directory)
```bash
npm install                    # Install dependencies
npm run dev                    # Start dev server (http://localhost:5173)
npm run build                  # Production build
# No lint/test configured. Manual: npx eslint src/ --fix
```

### Backend (in `backend/` directory)
```bash
python -m venv venv && .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env           # Fill in API keys

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
mypy app/ --ignore-missing-imports  # Optional
ruff check app/ --fix               # Optional
# No test framework. Tests would use pytest.
```

### Docker
```bash
docker-compose up --build      # Build and start
docker-compose down            # Stop
```

---

## Code Style Guidelines

### Backend (Python/FastAPI)

**Imports (ordered groups):**
```python
# 1. Standard library
import asyncio
from datetime import datetime
from typing import Any, Optional

# 2. Third-party
import httpx
from fastapi import APIRouter, HTTPException, Query

# 3. Local imports
from app.services.nullbr_service import nullbr_service
```

**Type Hints:**
- Use Python 3.10+ syntax: `list[dict]`, `str | None` (not `Optional[str]`)
- SQLAlchemy models: `Mapped[int]`, `Mapped[str | None]`
- Avoid bare `Any`

**Naming:**
- snake_case: functions, variables, modules
- PascalCase: classes, Pydantic models
- UPPER_SNAKE_CASE: constants
- Service singletons: `nullbr_service = NullbrService()`

**Async Patterns:**
- All I/O must be async
- Use `asyncio.to_thread()` for blocking sync calls

**Error Handling:**
```python
raise HTTPException(status_code=400, detail="Error message")

try:
    result = await tmdb_service.get_movie(tmdb_id)
except ValueError as exc:
    raise HTTPException(status_code=400, detail=str(exc))
except Exception as exc:
    raise HTTPException(status_code=502, detail=f"Request failed: {str(exc)}")
```

**Docstrings:**
```python
def get_movie(self, tmdb_id: int) -> dict:
    """Get movie details."""
```

### Frontend (Vue 3/JavaScript)

**Script Setup:**
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { searchApi } from '@/api'

const router = useRouter()
const loading = ref(false)
</script>
```

**Naming:**
- camelCase: variables, functions, props
- PascalCase: component files, imports
- kebab-case: templates

**API Pattern:**
```javascript
export const searchApi = {
  search: (query, page = 1) => api.get('/search', { params: { query, page } }),
}

const handleSearch = async () => {
  loading.value = true
  try {
    const { data } = await searchApi.search(keyword)
    results.value = data.items || []
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'Search failed')
  } finally {
    loading.value = false
  }
}
```

**Reactivity:**
- Use `ref()` for primitives and objects
- Use `computed()` for derived state
- Access refs with `.value` in script

### Styling (SCSS)
```scss
.component-name {
  padding: 16px;
  .nested-element { margin: 8px 0; }
  &:hover { opacity: 0.9; }
}
```

---

## Project Structure
```
MediaSync115/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── .env.example         # Environment template
│   └── app/
│       ├── api/             # Route handlers
│       ├── core/            # Config, database
│       ├── models/          # SQLAlchemy ORM
│       └── services/        # Business logic
├── frontend/
│   └── src/
│       ├── api/index.js     # Axios + API methods
│       ├── router/index.js  # Vue Router
│       └── views/           # Page components
└── docker-compose.yml
```

---

## Key Conventions

1. **Development Flow:** Add services → API routes → frontend API methods → UI components
2. **New Pages:** Create in `views/`, register in `router/index.js`
3. **Database:** Auto-created via SQLAlchemy; delete `data/mediasync.db` to reset
4. **Environment:** Copy `.env.example` to `.env` and fill in API keys

## Service URLs
- Backend API: http://localhost:8000
- Frontend Dev: http://localhost:5173
- API Docs: http://localhost:8000/docs

## Cursor/Copilot Rules
No Cursor rules (`.cursor/rules/` or `.cursorrules`) or Copilot rules (`.github/copilot-instructions.md`) are present in this repository.
