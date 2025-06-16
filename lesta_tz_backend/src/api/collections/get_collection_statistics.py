import math
import hashlib
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends, APIRouter,Query, Path
from pathlib import Path as FilePath
from collections import Counter
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models import Document, DocumentWord, CollectionDocument, Word, Collection
from src.utils import check_user_access, clean_text

from .schemas import DocumentStatisticsResponse

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/collections/{collection_id}/statistics", response_model=DocumentStatisticsResponse)
async def get_collection_statistics(
    collection_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100),
) -> DocumentStatisticsResponse:
    user = await check_user_access(token, session)
    user_id = user.id

    # Проверка принадлежности коллекции
    stmt = select(Collection).where(Collection.id == collection_id, Collection.owner_id == user_id)
    result = await session.execute(stmt)
    collection = result.scalar_one_or_none()
    if not collection:
        raise HTTPException(status_code=404, detail="Коллекция не найдена")

    # Получение документов коллекции
    stmt = (
        select(Document)
        .join(CollectionDocument, Document.id == CollectionDocument.document_id)
        .where(CollectionDocument.collection_id == collection_id)
    )
    result = await session.execute(stmt)
    documents = result.scalars().all()
    if not documents:
        raise HTTPException(status_code=400, detail="Коллекция пуста")

    document_ids = [doc.id for doc in documents]

    # Перепроверка и обновление TF-хэшей
    for document in documents:
        stmt = select(DocumentWord).where(DocumentWord.document_id == document.id)
        result = await session.execute(stmt)
        doc_words = result.scalars().all()

        try:
            with open(FilePath(document.file_path), "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            continue

        current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

        if not doc_words or document.content_hash != current_hash:
            words_list = clean_text(text)
            total_words = len(words_list)
            if total_words == 0:
                continue

            tf_counter = Counter(words_list)
            all_words = set(tf_counter.keys())

            result = await session.execute(select(Word).where(Word.text.in_(all_words)))
            existing_words = result.scalars().all()
            existing_word_map = {word.text: word.id for word in existing_words}
            new_words = list(all_words - existing_word_map.keys())

            if new_words:
                insert_stmt = insert(Word).returning(Word.id, Word.text)
                result = await session.execute(insert_stmt, [{"text": w} for w in new_words])
                for word_id, word_text in result.fetchall():
                    existing_word_map[word_text] = word_id

            await session.execute(delete(DocumentWord).where(DocumentWord.document_id == document.id))

            doc_words_data = [
                {
                    "document_id": document.id,
                    "word_id": existing_word_map[word],
                    "tf": round(count / total_words, 10),
                    "text": word
                }
                for word, count in tf_counter.items()
            ]
            await session.execute(insert(DocumentWord), doc_words_data)

            stmt = (
                update(Document)
                .where(Document.id == document.id)
                .values(content_hash=current_hash)
            )
            await session.execute(stmt)

            await session.commit()

    # Собираем общий список слов и их частот
    raw_word_counts = Counter()
    total_words = 0

    for document in documents:
        try:
            with open(FilePath(document.file_path), "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            continue

        words = clean_text(text)
        total_words += len(words)
        raw_word_counts.update(words)

    if total_words == 0:
        raise HTTPException(status_code=400, detail="Невозможно рассчитать TF по пустой коллекции")

    results = []
    total_docs = len(document_ids)

    for word_text, count in raw_word_counts.items():
        tf = round(count / total_words, 7)

        stmt = select(Word).where(Word.text == word_text)
        result = await session.execute(stmt)
        word_obj = result.scalar_one_or_none()
        if not word_obj:
            continue

        stmt = (
            select(DocumentWord.document_id)
            .where(
                DocumentWord.word_id == word_obj.id,
                DocumentWord.document_id.in_(document_ids)
            )
            .distinct()
        )
        result = await session.execute(stmt)
        df = len(result.scalars().all())

        idf = math.log10(total_docs / df) if df else 0.0

        results.append({
            "word": word_text,
            "tf": tf,
            "idf": round(idf, 10)
        })

    results.sort(key=lambda x: -x["idf"])
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = results[start:end]

    return DocumentStatisticsResponse(
        page=page,
        page_size=page_size,
        total=len(results),
        total_pages=math.ceil(len(results) / page_size),
        results=paginated_results
    )
