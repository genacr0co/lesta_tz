# from jose import jwt
# from datetime import datetime, timedelta, timezone
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from fastapi import HTTPException, status
# import random

# from .models import Users
# from .config import ALGORITHM, SECRET_KEY


# def generate_four_digit_code():
#     digits = random.sample("1234567890",4) # 4 элемента без повторов из заданной коллекции
#     number = int("".join(digits)) # соединяем в одно и конвертируем в число
#     if number < 1000: # если первая цифра была 0...
#         number = number * 10 # ...то добавляем его в конец

#     return number

# async def is_access_token_valid(access_token: str):
#     try:
#         token = access_token.credentials
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         exp = datetime.fromtimestamp(payload.get('exp'), tz=timezone.utc)
#         now = datetime.now(timezone.utc)
#         if exp > now:
#             return True
#         else:
#             return False
#     except:
#         return True


# def generate_number_with_id(id_number:int):
#     id_str = str(id_number)
#     zeros_needed = max(0, 12 - len(id_str))
#     generated_number = id_str + "0" * zeros_needed
#     return f'+{generated_number}'


# async def check_user_access(token: str,  session: AsyncSession):
#     if is_access_token_valid(token) == False:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     id: int = int(payload.get('id'))

#     user = await session.execute(select(Users).filter(Users.c.id == id))
#     user = user.fetchone()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     return user