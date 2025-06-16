from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func

from src.models import Collection
from src.db import get_async_session
from src.utils import check_user_access

from .schemas import CollectionListResponse, CollectionResponse

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/collections/", response_model=CollectionListResponse)
async def get_user_collections(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100)
):
    user = await check_user_access(token, session)

    stmt = (
        select(Collection)
        .where(Collection.owner_id == user.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    collections = result.scalars().all()

    count_stmt = select(func.count()).select_from(Collection).where(Collection.owner_id == user.id)
    count_result = await session.execute(count_stmt)
    total = count_result.scalar_one()

    return CollectionListResponse(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=(total + page_size - 1) // page_size,
        results=[CollectionResponse(id=col.id, name=col.name) for col in collections]
    )