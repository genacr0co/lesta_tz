from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.utils import check_user_access
from src.db import get_async_session
from src.models import Collection

from .schemas import CollectionResponse

router = APIRouter()
http_bearer = HTTPBearer()

@router.post("/collections", response_model=CollectionResponse, status_code=201)
async def create_collection(
    name: str = Body(..., embed=True),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
) -> CollectionResponse:
    user = await check_user_access(token, session)

    # Проверка уникальности имени
    stmt = select(Collection).where(Collection.owner_id == user.id, Collection.name == name)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Коллекция с таким именем уже существует")

    collection = Collection(name=name, owner_id=user.id)
    session.add(collection)
    await session.commit()
    await session.refresh(collection)

    return CollectionResponse(id=collection.id, name=collection.name)

