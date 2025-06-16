from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.db import get_async_session
from src.utils import check_user_access,hash_password
from src.models import Users

from .schemas import UserResponse, UserUpdateRequest

router = APIRouter()
http_bearer = HTTPBearer()

@router.patch("/user/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdateRequest,
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
)->UserResponse:
    user = await check_user_access(token, session)
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    update_data = {}
    if data.name is not None:
        update_data["name"] = data.name
    if data.email is not None:
        update_data["email"] = data.email
    if data.password is not None:
        update_data["password"] = hash_password(data.password)

    if update_data:
        stmt = (
            update(Users)
            .where(Users.id == user_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    stmt = select(Users).where(Users.id == user_id)
    result = await session.execute(stmt)
    updated_user = result.scalar_one()

    return updated_user