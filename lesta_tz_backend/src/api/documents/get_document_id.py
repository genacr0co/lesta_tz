from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os

from src.db import get_async_session
from src.utils import check_user_access
from src.models import Document

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/documents/{document_id}")
async def get_document_content(
    document_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
):
    user = await check_user_access(token, session)

    stmt = select(Document).where(Document.id == document_id, Document.owner_id == user.id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    # Проверка наличия файла на диске
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=500, detail="Файл не найден на сервере")

    # Чтение содержимого файла
    try:
        with open(document.file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении файла: {str(e)}")

    return {
        "id": document.id,
        "filename": document.filename,
        "content": content
    }