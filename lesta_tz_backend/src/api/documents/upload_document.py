from uuid import uuid4
import hashlib
from fastapi import HTTPException, UploadFile, File, Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path

from src.db import get_async_session
from src.models import Document
from src.utils import check_user_access

from .schemas import UploadResponse


router = APIRouter()
http_bearer = HTTPBearer()

STATIC_DIR = Path("static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
) -> UploadResponse:
    
     # Проверка токена и получение пользователя
    user = await check_user_access(token, session)
    user_id = user.id

    # Проверка расширения файла
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Можно загружать только .txt файлы")

    # Создаём директорию пользователя
    user_dir = STATIC_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    # Формируем путь к файлу
    file_location = user_dir / file.filename
    if file_location.exists():
        unique_prefix = uuid4().hex[:8]
        file_location = user_dir / f"{unique_prefix}_{file.filename}"

    file_content = await file.read()
    text = file_content.decode("utf-8")
    content_hash = hashlib.sha256(text.encode()).hexdigest()

    with open(file_location, "wb") as f:
        f.write(file_content)

    # Сохраняем документ в БД
    stmt = insert(Document).values(
        filename=file_location.name,
        file_path=str(file_location),
        owner_id=user_id,
        content_hash=content_hash
    ).returning(Document.id)
    result = await session.execute(stmt)
    doc_id = result.scalar()

    await session.commit()

    return UploadResponse(message="Файл загружен", document_id=doc_id)