from fastapi import APIRouter, Depends, HTTPException,Path
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.db import get_async_session
from src.utils import check_user_access
from src.models import Collection,CollectionDocument, Document

router = APIRouter()
http_bearer = HTTPBearer()

@router.delete("/collections/{collection_id}")
async def delete_collection(
    collection_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
):
    user = await check_user_access(token, session)

    # Загружаем коллекцию с её документами
    stmt = select(Collection).where(
        Collection.id == collection_id,
        Collection.owner_id == user.id
    ).options(
        selectinload(Collection.documents).selectinload(CollectionDocument.document)
    )
    result = await session.execute(stmt)
    collection = result.scalar_one_or_none()

    if not collection:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    # Сохраняем ID всех документов этой коллекции
    document_ids = [link.document_id for link in collection.documents]

    # Удаляем коллекцию (связи CollectionDocument удалятся каскадно)
    await session.delete(collection)
    await session.commit()

    # Проверяем, остались ли документы в других коллекциях
    for doc_id in document_ids:
        stmt = select(CollectionDocument).where(CollectionDocument.document_id == doc_id)
        result = await session.execute(stmt)
        other_links = result.scalars().all()

        if not other_links:
            # Документ больше нигде не используется — удаляем его и файл
            stmt = select(Document).where(Document.id == doc_id)
            result = await session.execute(stmt)
            doc = result.scalar_one_or_none()

            if doc:
                # Удаление физического файла
                if os.path.exists(doc.file_path):
                    os.remove(doc.file_path)

                await session.delete(doc)

    await session.commit()

    return {
        "detail": f"Коллекция {collection_id} удалена. Документы удалены, если больше нигде не использовались."
    }