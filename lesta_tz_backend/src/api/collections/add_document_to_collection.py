from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from src.models import Document, CollectionDocument, Collection
from src.db import get_async_session
from src.utils import check_user_access

router = APIRouter()
http_bearer = HTTPBearer()

@router.post("/collection/{collection_id}/{document_id}", status_code=201)
async def add_document_to_collection(
    collection_id: int,
    document_id: int,
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    user = await check_user_access(token, session)

    # Проверка существования коллекции и документа
    col_stmt = select(Collection).where(Collection.id == collection_id, Collection.owner_id == user.id)
    doc_stmt = select(Document).where(Document.id == document_id, Document.owner_id == user.id)

    col_res = await session.execute(col_stmt)
    doc_res = await session.execute(doc_stmt)

    collection = col_res.scalar_one_or_none()
    document = doc_res.scalar_one_or_none()

    if not collection or not document:
        raise HTTPException(status_code=404, detail="Коллекция или документ не найдены")

    # Попытка создать связь
    try:
        new_link = CollectionDocument(collection_id=collection_id, document_id=document_id)
        session.add(new_link)
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Документ уже находится в коллекции")

    return {
        "message": f"Документ {document.id} добавлен в коллекцию {collection.id}"
    }