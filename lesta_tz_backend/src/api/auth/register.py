from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from typing import Union, Any

from src.db import get_async_session
from src.models import Users
from src.utils import hash_password

from .schemas import UserCreate

router = APIRouter()

@router.post("/register")
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Union[Any]:
    result = await session.execute(select(Users).where(Users.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    hashed_password = hash_password(user_data.password)

    new_user = Users(
        email=user_data.email,
        name=user_data.name,
        password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email, "name": new_user.name}