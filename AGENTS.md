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
npm run preview                # Preview production build
```

**Note:** No lint/test commands are configured. Run linting manually if needed:
```bash
npx eslint src/ --fix          # Lint and fix (requires eslint setup)
npx prettier --write "src/**/*.{js,vue,scss}"  # Format code
```

### Backend (in `backend/` directory)

```bash
# Setup
python -m venv venv
.\venv\Scripts\activate        # Windows PowerShell
# source venv/bin/activate     # Linux/macOS
pip install -r requirements.txt

# Environment
copy .env.example .env         # Windows (then edit with real API keys)

# Development
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Type checking (optional, if mypy installed)
mypy app/ --ignore-missing-imports

# Linting (optional, if ruff installed)
ruff check app/ --fix
```

**Note:** No test framework is configured. Tests would use pytest if added.

### Docker

```bash
docker-compose up --build      # Build and start all services
docker-compose up -d           # Run in background
docker-compose down            # Stop services
```

---

## Code Style Guidelines

### Backend (Python/FastAPI)

**Imports:**
```python
# 1. Standard library
import asyncio
import hashlib
from datetime import datetime
from typing import Any, Optional

# 2. Third-party
import httpx
from fastapi import APIRouter, HTTPException, Query

# 3. Local imports
from app.services.nullbr_service import nullbr_service
from app.core.config import settings
```

**Type Hints:**
- Use modern Python 3.10+ syntax: `list[dict]`, `str | None` (not `Optional[str]`)
- Use `Mapped[]` for SQLAlchemy models: `Mapped[int]`, `Mapped[str | None]`

**Async Patterns:**
- All I/O operations must be async
- Use `asyncio.to_thread()` for blocking sync calls
- Database sessions must use async context

**Naming:**
- snake_case for functions, variables, modules
- PascalCase for classes
- UPPER_SNAKE_CASE for constants
- Service instances: `nullbr_service = NullbrService()` (singleton pattern)

**Error Handling:**
```python
# Use HTTPException for API errors
raise HTTPException(status_code=400, detail="Error message")

# Try/except with specific exceptions
try:
    result = await some_async_operation()
except Exception as exc:
    # Log and handle gracefully
    return {"error": str(exc)}
```

**Docstrings:**
```python
def get_movie(self, tmdb_id: int) -> dict:
    """
    Get movie details.

    Args:
        tmdb_id: TMDB ID

    Returns:
        Movie details dictionary
    """
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
const results = ref([])
</script>
```

**Naming:**
- camelCase for variables, functions, props
- PascalCase for component files and imports
- kebab-case in templates (`<el-button>`)

**API Pattern:**
```javascript
// Arrow function shorthand in api/index.js
export const searchApi = {
  search: (query, page = 1) => api.get('/search', { params: { query, page } }),
  getMovie: (tmdbId) => api.get(`/search/movie/${tmdbId}`),
}

// Usage in components
const handleSearch = async () => {
  loading.value = true
  try {
    const { data } = await searchApi.search(keyword)
    results.value = data.items || []
  } catch (error) {
    ElMessage.error('Search failed')
  } finally {
    loading.value = false
  }
}
```

**Reactivity:**
- Use `ref()` for primitive values and objects
- Use `computed()` for derived state
- Access refs with `.value` in script, without in template

**Error Handling:**
- Axios interceptor handles errors globally (shows ElMessage)
- Catch errors locally for special handling

### Styling (SCSS)

```scss
.component-name {
  padding: 16px;

  .nested-element {
    margin: 8px 0;
  }

  &:hover {
    opacity: 0.9;
  }
}
```

---

## Project Structure

```
MediaSync115/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt
│   ├── app/
│   │   ├── api/             # Route handlers
│   │   ├── core/            # Config, database
│   │   ├── models/          # SQLAlchemy ORM
│   │   └── services/        # Business logic
│   └── data/                # SQLite database
├── frontend/
│   ├── src/
│   │   ├── api/index.js     # Axios + API methods
│   │   ├── router/index.js  # Vue Router
│   │   ├── views/           # Page components
│   │   └── styles/          # Global SCSS
│   └── vite.config.js
└── docker-compose.yml
```

---

## Key Conventions

1. **Backend Routes:** Add services first, then API routes, then frontend API methods
2. **New Pages:** Create in `views/`, register in `router/index.js`
3. **Database:** Auto-created via SQLAlchemy; delete `data/mediasync.db` to reset
4. **Environment:** Copy `.env.example` to `.env` and fill in API keys

## Service URLs

- Backend API: http://localhost:8000
- Frontend Dev: http://localhost:5173
- API Docs: http://localhost:8000/docs (FastAPI Swagger)
