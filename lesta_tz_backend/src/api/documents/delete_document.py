import os
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db import get_async_session
from src.utils import check_user_access
from src.models import Document

router = APIRouter()
http_bearer = HTTPBearer()


@router.delete("/document/{document_id}", status_code=200)
async def delete_document(
    document_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
):
    user = await check_user_access(token, session)

    stmt = (
        select(Document)
        .where(Document.id == document_id, Document.owner_id == user.id)
        .options(selectinload(Document.collections))
    )
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    # Удаление файла с диска
    file_path = document.file_path
    if os.path.exists(file_path):
        os.remove(file_path)

    # Удаление связей
    for link in document.collections:
        await session.delete(link)

    # Удаление самого документа
    await session.delete(document)
    await session.commit()

    return {"detail": f"Документ '{document.filename}' и его файл удалены"}