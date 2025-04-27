import os
import sys
import string
import uuid

from fastapi import HTTPException, UploadFile, File, Depends, APIRouter

from sqlalchemy import select

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
from collections import Counter

sys.path.append(os.path.join(sys.path[0], 'src'))

from src.db import get_async_session
from src.models import Document, Word, DocumentWord

router = APIRouter()

STATIC_DIR = Path("static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(text: str):
    translator = str.maketrans('', '', string.punctuation)
    return text.lower().translate(translator).split()


@router.post("/upload")
async def upload(
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Можно загружать только текстовые (.txt) файлы")

    file_location = STATIC_DIR / file.filename

    #добавляем уникальный префикс
    if file_location.exists():
        unique_prefix = uuid.uuid4().hex[:8] 
        file_location = STATIC_DIR / f"{unique_prefix}_{file.filename}"

    file_content = await file.read()

    with open(file_location, "wb") as f:
        f.write(file_content)

    # Сохраняем путь файла в БД
    stmt = insert(Document).values(
        filename=file_location.name,
        file_path=str(file_location)
    ).returning(Document.id)
    result = await session.execute(stmt)
    doc_id = result.scalar()

    # Считаем tf слов в файле
    text = file_content.decode("utf-8")

    words_list = clean_text(text)
    total_words = len(words_list)
    if total_words == 0:
        raise HTTPException(status_code=400, detail="Файл не содержит слов после очистки текста")

    tf_counter = Counter(words_list)

    # Находим уже существующие слова
    all_words = set(tf_counter.keys())
    select_existing_stmt = select(Word).where(Word.text.in_(all_words))
    result = await session.execute(select_existing_stmt)
    existing_words = result.scalars().all()

    existing_word_map = {word.text: word.id for word in existing_words}
    new_words = list(all_words - set(existing_word_map.keys()))

    # Сохраняем новые слова
    new_word_objs = [{"text": text} for text in new_words]
    if new_word_objs:
        insert_words_stmt = insert(Word).returning(Word.id, Word.text)
        result = await session.execute(insert_words_stmt, new_word_objs)
        new_inserted_words = result.fetchall()

        for word_id, word_text in new_inserted_words:
            existing_word_map[word_text] = word_id

            
    document_words = [
        {
            "document_id": doc_id,
            "word_id": existing_word_map[word_text],
            "tf": ( count / total_words),
            "text": word_text
        }
        for word_text, count in tf_counter.items()
    ]

    insert_doc_words_stmt = insert(DocumentWord)
    await session.execute(insert_doc_words_stmt, document_words)

    await session.commit()

    return {"message": "Файл загружен", "document_id": doc_id}