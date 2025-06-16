from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import shutil
from pathlib import Path as FilePath

from src.models import Users
from src.db import get_async_session
from src.utils import check_user_access

router = APIRouter()
http_bearer = HTTPBearer()
@router.delete("/user/{user_id}", status_code=200)
async def delete_user(
    user_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
):
    # Проверка прав доступа
    user = await check_user_access(token, session)
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    # Проверка, что пользователь существует
    stmt = select(Users).where(Users.id == user_id)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Удаление пользователя
    await session.delete(existing_user)

    # Удаление папки с файлами
    user_dir = FilePath(f"static/{user_id}")
    if user_dir.exists() and user_dir.is_dir():
        shutil.rmtree(user_dir)

    await session.commit()
    
    return {"detail": "Пользователь успешно удалён"}