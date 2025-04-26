import re
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request

import requests
from sqlalchemy import select, update, delete

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from typing import Tuple, Union, Any
import os
import sys
from fastapi import Query
from math import ceil
from sqlalchemy import func
from sqlalchemy import and_

from datetime import datetime, timezone
import time

sys.path.append(os.path.join(sys.path[0], 'src'))


from src.utils import generate_four_digit_code, generate_number_with_id
from src.db import get_async_session
from src.models import Words
from src.app.schemas import CompleteTaskRequestBody, CloseShiftRequestBody, OpenShiftRequestBody

router = APIRouter(
    prefix="/api",
    tags=["Lesta TF_IDF API"],
)


@router.get('/words', description='Get words tf_idf list')
async def get_user(session: AsyncSession = Depends(get_async_session)) -> Union[Any]:
    
    return {
        "hello": "world"
    }
    # existing_user = await session.execute(select(Users).where(Users.c.phone == phone))
    # existing_user = existing_user.fetchone()



    # if existing_user:
    #     role_id = existing_user[3]
    #     role = await session.execute(select(Roles).where(Roles.c.id == role_id))
    #     role = role.fetchone()

    #     data = {
    #         "id": existing_user[0],
    #         "phone": existing_user[1],
    #         "name": existing_user[2],
    #         "topic_id": existing_user[4],
    #         "role": {
    #             "id": role[0],
    #             "name": role[1]
    #         }
    #     }

    #     return data
    # else:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")