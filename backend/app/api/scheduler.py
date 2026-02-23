import json
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.scheduler_task import SchedulerTask
from app.scheduler import scheduler_manager
from app.services.job_registry import job_registry

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


class SchedulerTaskCreate(BaseModel):
    name: str
    job_key: str
    trigger_type: str = "cron"
    cron_expr: Optional[str] = None
    interval_seconds: Optional[int] = None
    kwargs: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


class SchedulerTaskUpdate(BaseModel):
    name: Optional[str] = None
    job_key: Optional[str] = None
    trigger_type: Optional[str] = None
    cron_expr: Optional[str] = None
    interval_seconds: Optional[int] = None
    kwargs: Optional[dict[str, Any]] = None
    enabled: Optional[bool] = None


@router.get("/job-keys")
async def list_job_keys():
    return {"items": job_registry.list_keys()}


@router.get("/jobs")
async def list_scheduler_jobs():
    return {"items": scheduler_manager.list_jobs()}


@router.post("/run/{job_id}")
async def run_scheduler_job(job_id: str):
    result = await scheduler_manager.run_now(job_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message") or "run failed")
    return result


@router.get("/tasks")
async def list_dynamic_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SchedulerTask).order_by(SchedulerTask.created_at.desc()))
    return result.scalars().all()


@router.post("/tasks")
async def create_dynamic_task(payload: SchedulerTaskCreate, db: AsyncSession = Depends(get_db)):
    if not job_registry.get(payload.job_key):
        raise HTTPException(status_code=400, detail=f"Unknown job_key: {payload.job_key}")

    task = SchedulerTask(
        name=payload.name,
        job_key=payload.job_key,
        trigger_type=payload.trigger_type,
        cron_expr=payload.cron_expr,
        interval_seconds=payload.interval_seconds,
        kwargs_json=json.dumps(payload.kwargs or {}, ensure_ascii=False),
        enabled=payload.enabled,
        state="W" if payload.enabled else "P",
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    await scheduler_manager.update_dynamic_job(task)
    return task


@router.put("/tasks/{task_id}")
async def update_dynamic_task(task_id: int, payload: SchedulerTaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await db.get(SchedulerTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)
    if "job_key" in data and data["job_key"] and not job_registry.get(data["job_key"]):
        raise HTTPException(status_code=400, detail=f"Unknown job_key: {data['job_key']}")

    if "kwargs" in data:
        task.kwargs_json = json.dumps(data.pop("kwargs") or {}, ensure_ascii=False)

    for key, value in data.items():
        setattr(task, key, value)

    if task.enabled and task.state == "P":
        task.state = "W"
    if not task.enabled:
        task.state = "P"

    await db.commit()
    await db.refresh(task)

    await scheduler_manager.update_dynamic_job(task)
    if not task.enabled:
        await scheduler_manager.remove_dynamic_job(task.id)
    return task


@router.post("/tasks/{task_id}/enable")
async def enable_dynamic_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(SchedulerTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.enabled = True
    task.state = "W"
    await db.commit()
    await db.refresh(task)
    await scheduler_manager.update_dynamic_job(task)
    return {"success": True}


@router.post("/tasks/{task_id}/pause")
async def pause_dynamic_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(SchedulerTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.enabled = False
    task.state = "P"
    await db.commit()
    await db.refresh(task)
    await scheduler_manager.remove_dynamic_job(task.id)
    return {"success": True}


@router.delete("/tasks/{task_id}")
async def delete_dynamic_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(SchedulerTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    await scheduler_manager.remove_dynamic_job(task_id)
    return {"success": True}
