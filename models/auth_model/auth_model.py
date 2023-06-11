import uuid
from datetime import timedelta
from typing import Union

from pydantic import BaseModel


class UserView(BaseModel):
    """DATA CLASS FOR CREATING MODEL IN GET_CURRENT_USER FUNCTION"""
    u_uuid: Union[str, uuid.UUID]
    u_username: str


class PayloadToken(BaseModel):
    exp: timedelta
    sub: Union[str, uuid.UUID]
