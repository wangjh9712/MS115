# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在此项目中工作时提供指导。

## 项目概述

MediaSync115 是一个全栈媒体同步应用，通过 Nullbr API（基于 TMDB）搜索电影/电视剧，管理订阅，并与 115 网盘集成进行文件管理和离线下载。

## 技术栈

- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia + Axios + SCSS
- **后端**: FastAPI + SQLAlchemy (异步) + SQLite (aiosqlite) + Pydantic Settings
- **部署**: Docker + Nginx

## 开发命令

### 前端
```bash
cd frontend
npm install
npm run dev      # 开发服务器
npm run build    # 生产构建
npm run preview  # 预览生产构建
```

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker
```bash
docker-compose up --build
```
- 后端: http://localhost:8000
- 前端: http://localhost

## 架构

### 前端结构 (`frontend/src/`)
- `views/` - 页面组件：Search、Subscriptions、Downloads、Settings、MovieDetail、TvDetail
- `api/` - 基于 Axios 的 API 客户端
- `router/` - Vue Router 配置
- `styles/` - SCSS 样式文件

路由：
- `/` → 重定向到 `/search`
- `/search` → 媒体搜索
- `/subscriptions` → 订阅管理
- `/downloads` → 下载历史
- `/settings` → 应用设置
- `/movie/:id` → 电影详情
- `/tv/:id` → 电视剧详情

### 后端结构 (`backend/app/`)
- `api/` - REST 接口：search、subscriptions、pan115
- `models/` - SQLAlchemy 模型：Subscription、DownloadRecord
- `services/` - 业务逻辑：nullbr_service、pan115_service
- `core/` - 配置和数据库设置

### 外部 API
- **Nullbr API** - 媒体搜索（基于 TMDB），通过 `NULLBR_APP_ID` 和 `NULLBR_API_KEY` 配置
- **115 网盘 API** - 文件管理和离线下载，通过 `PAN115_COOKIE` 配置

## 环境变量

从 `.env.example` 创建 `backend/.env`：
- `NULLBR_APP_ID` / `NULLBR_API_KEY` - Nullbr API 凭证
- `PAN115_COOKIE` - 115 网盘 Cookie
- `DATABASE_URL` - SQLite 连接（默认为 `sqlite+aiosqlite:///data/mediasync.db`）
- `DEBUG` - 调试模式标志
