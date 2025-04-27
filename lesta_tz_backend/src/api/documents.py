import os
import sys

from fastapi import Depends, APIRouter

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union


sys.path.append(os.path.join(sys.path[0], 'src'))

from src.db import get_async_session
from src.models import Document

router = APIRouter()

@router.get("/documents")
async def list_documents(session: AsyncSession = Depends(get_async_session)) -> Union[dict]:
    stmt = select(Document)
    result = await session.execute(stmt)
    docs = result.scalars().all()

    return {"results": [{"id": doc.id, "filename": doc.filename} for doc in docs]}