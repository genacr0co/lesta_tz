from fastapi import APIRouter, Query, Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models import Document
from src.utils import check_user_access

from .schemas import PaginatedDocumentsResponse,DocumentResponse

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/documents/", response_model=PaginatedDocumentsResponse)
async def get_user_documents(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100)
) -> PaginatedDocumentsResponse:
    user = await check_user_access(token, session)

    stmt = select(Document).where(Document.owner_id == user.id)
    result = await session.execute(stmt)
    documents = result.scalars().all()

    total = len(documents)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_docs = documents[start:end]

    # 👇 Преобразование ORM-моделей в Pydantic
    document_responses = [DocumentResponse.model_validate(doc) for doc in paginated_docs]

    return PaginatedDocumentsResponse(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=(total + page_size - 1) // page_size,
        documents=document_responses
    )