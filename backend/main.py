from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.core.database import init_db
from app.api import search, subscriptions, pan115, pansou, settings as runtime_settings_api, scheduler, workflow
from app.scheduler import scheduler_manager
from app.services.pansou_service import pansou_service
from app.services.runtime_settings_service import runtime_settings_service
from app.services.subscription_scheduler_service import subscription_scheduler_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("data", exist_ok=True)
    pansou_service.set_base_url(runtime_settings_service.get_pansou_base_url())
    await init_db()
    await scheduler_manager.init()
    await subscription_scheduler_service.ensure_subscription_tasks()
    yield
    await scheduler_manager.stop()
    await pansou_service.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api")
app.include_router(subscriptions.router, prefix="/api")
app.include_router(pan115.router, prefix="/api")
app.include_router(pansou.router, prefix="/api")
app.include_router(runtime_settings_api.router, prefix="/api")
app.include_router(scheduler.router, prefix="/api")
app.include_router(workflow.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
