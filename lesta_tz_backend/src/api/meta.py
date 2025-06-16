from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional, Union

from src.db import get_async_session
from src.models import AppMetrics
from src.config import APP_VERSION

router = APIRouter()

@router.get("/status")
async def health_check():
    return JSONResponse(content={"status": "OK"})


@router.get("/version")
async def get_version():
    return JSONResponse(content={"version": APP_VERSION})


async def update_metrics(
    session: AsyncSession,
    time_taken: float,
    user_id: int,
    user_name: str,
    file_size: int,
    file_name: str,
    file_path: str
):
    stmt = select(AppMetrics).limit(1)
    result = await session.execute(stmt)
    metrics = result.scalar_one_or_none()

    if not metrics:
        metrics = AppMetrics(
            files_processed=1,
            min_time_processed=round(time_taken, 3),
            avg_time_processed=round(time_taken, 3),
            max_time_processed=round(time_taken, 3),
            latest_file_processed_timestamp=datetime.utcnow(),
            last_user_id=user_id,
            last_user_name=user_name,
            last_file_size=file_size,
            last_file_name=file_name,
            last_file_path=file_path
        )
        session.add(metrics)
    else:
        files_processed = metrics.files_processed + 1
        total_time = metrics.avg_time_processed * metrics.files_processed + time_taken
        avg_time = total_time / files_processed

        metrics.files_processed = files_processed
        metrics.avg_time_processed = round(avg_time, 3)
        metrics.min_time_processed = round(min(metrics.min_time_processed, time_taken), 3)
        metrics.max_time_processed = round(max(metrics.max_time_processed, time_taken), 3)
        metrics.latest_file_processed_timestamp = datetime.utcnow()
        metrics.last_user_id = user_id
        metrics.last_user_name = user_name
        metrics.last_file_size = file_size
        metrics.last_file_name = file_name
        metrics.last_file_path = file_path

    await session.commit()

class MetricsResponse(BaseModel):
    files_processed: int
    min_time_processed: float
    avg_time_processed: float
    max_time_processed: float
    latest_file_processed_timestamp: Optional[int]
    last_user_id: Optional[int]
    last_user_name: Optional[str]
    last_file_size: Optional[int]
    last_file_name: Optional[str]
    last_file_path: Optional[str]

    
@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(session: AsyncSession = Depends(get_async_session)):
    stmt = select(AppMetrics).limit(1)
    result = await session.execute(stmt)
    metrics = result.scalar_one_or_none()

    if not metrics:
        return MetricsResponse(
            files_processed=0,
            min_time_processed=0.0,
            avg_time_processed=0.0,
            max_time_processed=0.0,
            latest_file_processed_timestamp=None,
            last_user_id=None,
            last_user_name=None,
            last_file_size=None,
            last_file_name=None,
            last_file_path=None
        )

    return MetricsResponse(
        files_processed=metrics.files_processed,
        min_time_processed=metrics.min_time_processed,
        avg_time_processed=metrics.avg_time_processed,
        max_time_processed=metrics.max_time_processed,
        latest_file_processed_timestamp=int(metrics.latest_file_processed_timestamp.timestamp()) if metrics.latest_file_processed_timestamp else None,
        last_user_id=metrics.last_user_id,
        last_user_name=metrics.last_user_name,
        last_file_size=metrics.last_file_size,
        last_file_name=metrics.last_file_name,
        last_file_path=metrics.last_file_path
    )