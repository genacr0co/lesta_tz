import random
import aiosmtplib
from email.message import EmailMessage

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional
from pydantic import EmailStr

from src.models import Users
from src.config import REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, SENDER_EMAIL, SMTP_PORT, SMTP_HOST, SMTP_PASSWORD, SMTP_USER

from .schemas import User

async def get_user_by_email(email: EmailStr, session: AsyncSession) -> Optional[User]:
    result = await session.execute(select(Users).filter(Users.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    result = await session.execute(select(Users).filter(Users.id == user_id))
    return result.scalar_one_or_none()

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens(user_id: int, email: EmailStr) -> Tuple[str, str]:
    now = datetime.now(timezone.utc)
    refresh_expires = timedelta(days=float(REFRESH_TOKEN_EXPIRE_DAYS))

    payload = {"sub": email, "id": user_id, "iat": now}
    access_token = create_jwt_token(payload)
    refresh_token = create_jwt_token(payload, expires_delta=refresh_expires)

    return access_token, refresh_token


def generate_four_digit_code():
    digits = random.sample("1234567890",4)
    number = int("".join(digits))
    if number < 1000: 
        number = number * 10

    return number


async def send_email(to_email: str, subject: str, body: str) -> bool:
    message = EmailMessage()
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST, 
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True, 
        )
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False