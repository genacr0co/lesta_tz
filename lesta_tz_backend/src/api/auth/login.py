from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from src.db import get_async_session

from .schemas import  Token, LoginRequestBody
from .utils import create_tokens, get_user_by_email

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=Token)
async def login_for_access_token(
    body: LoginRequestBody,
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    user = await get_user_by_email(body.email, session)

    if not user or not pwd_context.verify(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token, refresh_token = create_tokens(user.id, user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)