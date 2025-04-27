import os
import sys

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
from pathlib import Path


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



@router.get("/document/{document_id}/content")
async def get_document_content(
    document_id: int, 
    session: AsyncSession = Depends(get_async_session)
) -> dict:
   
    stmt = select(Document).where(Document.id == document_id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

   
    file_path = Path(document.file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл документа не найден на сервере")


    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файла: {str(e)}")

    return {
        "filename": document.filename,
        "content": content
    }