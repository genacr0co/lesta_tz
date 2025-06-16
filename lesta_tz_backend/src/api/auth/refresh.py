
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Any


from src.db import get_async_session
from src.config import SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS

from .utils import create_jwt_token, get_user_by_id
from .schemas import Token 


router = APIRouter()
http_bearer = HTTPBearer()

@router.post("/token/refresh", response_model=Token)
async def refresh_token(
    refresh_token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
) -> Union[Token, Any]:
    token_str = refresh_token.credentials

    try:
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("id"))
        exp_timestamp = payload.get("exp")

        if not user_id or not exp_timestamp:
            raise HTTPException(status_code=400, detail="Invalid token payload")

        user = await get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        if exp <= now:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Generate new tokens
        refresh_token_expires = timedelta(days=float(REFRESH_TOKEN_EXPIRE_DAYS))
        now_utc = datetime.now(timezone.utc)

        new_refresh_token = create_jwt_token(
            data={"sub": user.email, "id": user.id, "iat": now_utc},
            expires_delta=refresh_token_expires,
        )
        new_access_token = create_jwt_token(
            data={"sub": user.email, "id": user.id, "iat": now_utc}
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")