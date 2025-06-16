from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.utils import check_user_access

from .schemas import UserResponse

router = APIRouter()

http_bearer = HTTPBearer()

@router.get("/user", response_model=UserResponse)
async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
) -> UserResponse:
    user = await check_user_access(token, session)
    return user  