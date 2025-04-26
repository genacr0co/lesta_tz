from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from typing import Optional, Union
import re

import os
import sys

sys.path.append(os.path.join(sys.path[0], 'src'))

from src.schemas_validation import *

# class RegistrationRequestBody(
#         ValidatePhone, 
#         ValidateUserName,
#         BaseModel
#     ):
#     phone: str
#     name: Optional[str] = None 
#     username: Optional[str] = None 
#     birthday: Optional[datetime] = None 


class CompleteTaskRequestBody(ValidatePhone, BaseModel):
    phone: str
    subsection_id: int


class CloseShiftRequestBody(BaseModel):
    user_id: int

class OpenShiftRequestBody(BaseModel):
    user_id: int



# class EditUser(BaseModel):
#     phone: str
#     name: Optional[str] = None 
#     username: Optional[str] = None 
#     birthday: Optional[datetime] = None 



# class LoginRequestBody(ValidatePhone, BaseModel):
#     phone: str
#     code: int

# class PwcCodeRequestBody(ValidatePhone, BaseModel):
#     phone: str

# class User(BaseModel):
#     id: int
#     phone: str
#     name: str
#     username: str
#     birthday: datetime




# class Token(BaseModel):
#     access_token: str
#     refresh_token: str

# class PwcCodeResponse(BaseModel):
#     phone: str
#     pwc_code: str