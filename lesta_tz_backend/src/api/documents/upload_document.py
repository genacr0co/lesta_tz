from uuid import uuid4
import time
import hashlib
from fastapi import HTTPException, UploadFile, File, Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path

from src.db import get_async_session
from src.models import Document
from src.utils import check_user_access
from src.api.meta import update_metrics

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
    start_time = time.perf_counter()

    user = await check_user_access(token, session)
    user_id = user.id

    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Можно загружать только .txt файлы")

    user_dir = STATIC_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    file_location = user_dir / file.filename
    if file_location.exists():
        unique_prefix = uuid4().hex[:8]
        file_location = user_dir / f"{unique_prefix}_{file.filename}"

    file_content = await file.read()
    text = file_content.decode("utf-8")
    content_hash = hashlib.sha256(text.encode()).hexdigest()

    with open(file_location, "wb") as f:
        f.write(file_content)

    stmt = insert(Document).values(
        filename=file_location.name,
        file_path=str(file_location),
        owner_id=user_id,
        content_hash=content_hash
    ).returning(Document.id)
    result = await session.execute(stmt)
    doc_id = result.scalar()

    # ⏱️ Время обработки
    elapsed_time = time.perf_counter() - start_time

    # 📊 Обновляем метрики
    await update_metrics(
        session=session,
        time_taken=elapsed_time,
        user_id=user.id,
        user_name=user.name,
        file_size=len(file_content),
        file_name=file_location.name,
        file_path=str(file_location)
    )

    await session.commit()

    return UploadResponse(message="Файл загружен", document_id=doc_id)