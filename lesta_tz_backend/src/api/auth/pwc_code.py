from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Any
from sqlalchemy import update

from src.db import get_async_session
from src.models import Users

from .schemas import PwcCodeRequestBody, PwcCodeResponse
from .utils import get_user_by_email, generate_four_digit_code, send_email

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


    subject = "Код подтверждения регистрации"
    message = (
        f"Здравствуйте, {user.name}!\n\n"
        f"Ваш код подтверждения: {pwc_code}\n"
        f"Введите его в форме авторизации на grenka.uz.\n\n"
        f"С уважением,\n grenka.uz"
    )

    # Отправляем письмо
    sent = await send_email(to_email=user.email, subject=subject, body=message)
    if not sent:
        raise HTTPException(status_code=500, detail="Ошибка при отправке email")

    return {"email": user.email, "pwc_code": pwc_code}
