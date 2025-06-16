import math
import hashlib

from pathlib import Path as FilePath
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends, APIRouter,Query,Path
from collections import Counter
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models import Document, DocumentWord, CollectionDocument, Word
from src.utils import check_user_access, clean_text

from .schemas import DocumentStatisticsResponse

router = APIRouter()
http_bearer = HTTPBearer()

@router.get("/document/{document_id}/statistics", response_model=DocumentStatisticsResponse)
async def get_document_statistics(
    document_id: int = Path(..., ge=1),
    collection_id: int | None = Query(None),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100),
) -> DocumentStatisticsResponse:
    user = await check_user_access(token, session)
    user_id = user.id

    # Получаем документ и проверяем владельца
    stmt = select(Document).where(Document.id == document_id, Document.owner_id == user_id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    # Загружаем содержимое файла
    try:
        with open(FilePath(document.file_path), "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Файл не найден на сервере")

    current_hash = hashlib.sha256(text.encode()).hexdigest()

    # Получаем существующие TF
    stmt = select(DocumentWord).where(DocumentWord.document_id == document_id).options(selectinload(DocumentWord.word))
    result = await session.execute(stmt)
    doc_words = result.scalars().all()

    if not doc_words or document.content_hash != current_hash:
        # Удалим старые TF
        await session.execute(delete(DocumentWord).where(DocumentWord.document_id == document_id))

        words_list = clean_text(text)
        total_words = len(words_list)
        if total_words == 0:
            raise HTTPException(status_code=400, detail="Файл не содержит слов после очистки")

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

        doc_words_data = [
            {
                "document_id": document_id,
                "word_id": existing_word_map[word],
                "tf": round(count / total_words, 7),
                "text": word
            }
            for word, count in tf_counter.items()
        ]
        await session.execute(insert(DocumentWord), doc_words_data)

        # Обновим хеш
        document.content_hash = current_hash
        session.add(document)
        await session.commit()

        # Повторно загружаем TF-данные
        stmt = select(DocumentWord).where(DocumentWord.document_id == document_id).options(selectinload(DocumentWord.word))
        result = await session.execute(stmt)
        doc_words = result.scalars().all()

    # Получение ID документов для расчёта IDF
    if collection_id:
        stmt = select(CollectionDocument).where(
            CollectionDocument.document_id == document_id,
            CollectionDocument.collection_id == collection_id
        )
        result = await session.execute(stmt)
        link = result.scalar_one_or_none()
        if not link:
            raise HTTPException(status_code=400, detail="Документ не принадлежит указанной коллекции")

        stmt = select(CollectionDocument.document_id).where(CollectionDocument.collection_id == collection_id)
        result = await session.execute(stmt)
        relevant_doc_ids = [row[0] for row in result.fetchall()]
    else:
        subq = select(CollectionDocument.document_id).subquery()
        stmt = select(Document.id).where(
            Document.owner_id == user_id,
            ~Document.id.in_(select(subq))
        )
        result = await session.execute(stmt)
        relevant_doc_ids = [row[0] for row in result.fetchall()]

    total_docs = len(relevant_doc_ids)
    if total_docs == 0:
        raise HTTPException(status_code=400, detail="Нет документов для расчёта IDF")

    # Расчёт IDF + сбор статистики
    results = []
    for doc_word in doc_words:
        word_text = doc_word.word.text
        tf = doc_word.tf

        stmt = (
            select(DocumentWord.document_id)
            .where(
                DocumentWord.word_id == doc_word.word_id,
                DocumentWord.document_id.in_(relevant_doc_ids)
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

    # Сортировка и пагинация
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