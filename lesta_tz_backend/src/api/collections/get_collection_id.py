import math
from fastapi import APIRouter, Depends, HTTPException, Query,Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from src.db import get_async_session
from src.models import Document, CollectionDocument, Collection
from src.utils import check_user_access

from .schemas import PaginatedDocumentsResponse, DocumentResponse

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/collections/{collection_id}", response_model=PaginatedDocumentsResponse)
async def get_collection_documents(
    collection_id: int = Path(..., ge=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
)->PaginatedDocumentsResponse:
    user = await check_user_access(token, session)

    # Проверка прав на коллекцию
    stmt = select(Collection).where(Collection.id == collection_id, Collection.owner_id == user.id)
    result = await session.execute(stmt)
    collection = result.scalar_one_or_none()
    if not collection:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    # Подсчёт общего количества документов
    count_stmt = select(func.count()).select_from(
        CollectionDocument
    ).where(CollectionDocument.collection_id == collection_id)
    total = await session.scalar(count_stmt)

    if total == 0:
        return PaginatedDocumentsResponse(
            page=page,
            page_size=page_size,
            total=0,
            total_pages=0,
            documents=[]
        )

    # Получение документов с пагинацией
    stmt = (
        select(Document)
        .join(CollectionDocument, CollectionDocument.document_id == Document.id)
        .where(CollectionDocument.collection_id == collection_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    documents = result.scalars().all()

    return PaginatedDocumentsResponse(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=math.ceil(total / page_size),
        documents=[
            DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                file_path=doc.file_path,
                owner_id=doc.owner_id
            )
            for doc in documents
        ]
    )