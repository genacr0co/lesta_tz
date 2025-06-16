from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_session

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/logout")
async def logout(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}