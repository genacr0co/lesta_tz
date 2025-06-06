from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session

from .schemas import  Token, LoginRequestBody
from .utils import create_tokens, get_user_by_email

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    body: LoginRequestBody,
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    user = await get_user_by_email(body.email, session)

    if not user or user.pwc_code is None or int(body.pwc_code) != int(user.pwc_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid credentials"
        )

    access_token, refresh_token = create_tokens(user.id, user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)