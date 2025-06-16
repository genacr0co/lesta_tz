from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.utils import check_user_access
from src.db import get_async_session
from src.models import Collection, CollectionDocument, Document

router = APIRouter()
http_bearer = HTTPBearer()
@router.delete("/collection/{collection_id}/{document_id}", status_code=200)
async def remove_document_from_collection(
    collection_id: int,
    document_id: int,
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
):
    user = await check_user_access(token, session)

    stmt = select(CollectionDocument).join(Collection).where(
        Collection.id == collection_id,
        Collection.owner_id == user.id,
        CollectionDocument.document_id == document_id
    )
    result = await session.execute(stmt)
    link = result.scalar_one_or_none()

    if not link:
        raise HTTPException(status_code=404, detail="Документ не найден в коллекции")

    # Получим имя документа и коллекции для сообщения
    doc_stmt = select(Document).where(Document.id == document_id)
    col_stmt = select(Collection).where(Collection.id == collection_id)

    doc_result = await session.execute(doc_stmt)
    col_result = await session.execute(col_stmt)
    document = doc_result.scalar_one_or_none()
    collection = col_result.scalar_one_or_none()

    await session.delete(link)
    await session.commit()

    return {
        "message": f"Документ «{document.filename if document else document_id}» удалён из коллекции «{collection.name if collection else collection_id}»"
    }