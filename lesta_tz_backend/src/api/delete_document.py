
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from src.db import get_async_session
from src.models import Document, DocumentWord

router = APIRouter()

@router.delete("/document/{document_id}")
async def delete_document(document_id: int, session: AsyncSession = Depends(get_async_session)):

    stmt = select(Document).where(Document.id == document_id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    

    delete_doc_words_stmt = delete(DocumentWord).where(DocumentWord.document_id == document_id)
    await session.execute(delete_doc_words_stmt)


    delete_document_stmt = delete(Document).where(Document.id == document_id)
    await session.execute(delete_document_stmt)

    file_path = Path(document.file_path)
    if file_path.exists():
        file_path.unlink() 
    
  
    await session.commit()

    return {"message": f"Документ и его слова успешно удалены (id={document_id})"}