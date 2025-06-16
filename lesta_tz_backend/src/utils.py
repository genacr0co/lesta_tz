import string
from jose import JWTError, jwt
from typing import Optional
from fastapi import HTTPException, status
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext

from .models import Users
from .config import ALGORITHM, SECRET_KEY


def clean_text(text: str):
    translator = str.maketrans('', '', string.punctuation)
    return text.lower().translate(translator).split()

# Получение payload из токена
def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# Проверка валидности access_token (срок действия)
def is_access_token_valid(token: str) -> bool:
    try:
        payload = decode_jwt_token(token)
        exp = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        return exp > datetime.now(timezone.utc)
    except Exception:
        return False


# Проверка пользователя по access_token
async def check_user_access(
    token: HTTPAuthorizationCredentials,
    session: AsyncSession
) -> Users:
    if not is_access_token_valid(token.credentials):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    payload = decode_jwt_token(token.credentials)
    user_id = payload.get("id")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    result = await session.execute(select(Users).where(Users.id == int(user_id)))
    user: Optional[Users] = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user





def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)