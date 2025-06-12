from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Any
from sqlalchemy import update

from src.db import get_async_session
from src.models import Users

from .schemas import PwcCodeRequestBody, PwcCodeResponse
from .utils import get_user_by_email, generate_four_digit_code

router = APIRouter()


# pwc code
@router.post("/pwc_code")
async def pwc_code(body: PwcCodeRequestBody, session: AsyncSession = Depends(get_async_session)) -> Union[PwcCodeResponse, Any]:
    user = await get_user_by_email(body.email, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    pwc_code = generate_four_digit_code()
    stmt = update(Users).where(Users.id == user.id).values(pwc_code=int(pwc_code))

    await session.execute(stmt)
    await session.commit()

    return {"email": user.email, "pwc_code": pwc_code}
