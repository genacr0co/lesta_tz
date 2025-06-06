import math

from fastapi import Depends, Query, APIRouter

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models import Document, DocumentWord

router = APIRouter()

@router.get("/document/{document_id}/words")
async def get_document_words(
    document_id: int, 
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100), 
) -> dict:
  
    stmt = select(Document)
    result = await session.execute(stmt)
    total_docs = len(result.scalars().all()) 

    stmt = select(DocumentWord).filter_by(document_id=document_id).options(selectinload(DocumentWord.word))
    result = await session.execute(stmt)
    doc_words = result.scalars().all()

    results = []
    for doc_word in doc_words:
        word_text = doc_word.word.text
        tf = doc_word.tf
      
        stmt = select(DocumentWord).filter(DocumentWord.word_id == doc_word.word_id).distinct(DocumentWord.document_id)
        result = await session.execute(stmt)
        df = len(result.scalars().all())
 
        idf = math.log10(total_docs / df)

        results.append({
            "word": word_text,
            "tf": tf,
            "idf": round(idf, 10)
        })
    
    results.sort(key=lambda x: -x["idf"])
   
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = results[start:end]

    return {
        "page": page,
        "page_size": page_size,
        "total": len(results),
        "total_pages": math.ceil(len(results) / page_size),
        "results": paginated_results
    }