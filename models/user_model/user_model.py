import re
import uuid
from typing import Union
from pydantic import BaseModel, Field, validator, ValidationError, validate_email


class UserInfo(BaseModel):
    """DATA CLASS USED FOR RETURNING INFO AFTER CHECKING PASSWORD
       WITH THIS WE CREATE TOKENS"""
    u_uuid: Union[str, uuid.UUID]
    u_username: str


class AccountRegModel(BaseModel):
    """Model for registration fields"""
    acc_contact_name: str
    acc_org_name: str
    acc_email: str
    acc_pass: str
    acc_phone: str
    acc_address: str | None
    acc_country: int = Field(default=1)
    acc_inn: str | None = Field(default=None, description="Идентификационный номер налогоплательщика", regex=r'\d{1,15}')
    acc_kpp: str | None = Field(default=None, description="код причины постановки", regex=r'\d{1,15}')
    acc_bik: str | None = Field(default=None, description="Бик (банковский идентификационный код)", regex=r'\d{1,15}')
    acc_bank_name: str | None = Field(default=None, description="", regex=r'\w{1,40}')
    acc_k_schet: str | None = Field(default=None, description="К/счет (корреспондентский счет)", regex=r'\d{20}')
    acc_r_schet: str | None = Field(default=None, description="Р/счет (расчетный счет)", regex=r'\d{20}')

    @validator('acc_phone')
    def check_acc_phone(cls, acc_phone):
        try:
            if re.match(r'\+374\d{8}', acc_phone):
                return acc_phone
        except Exception:
            raise ValidationError('PHONE ERROR')

    @validator('acc_email')
    def check_acc_email(cls, acc_email):
        try:
            if validate_email(acc_email):
                return acc_email
        except Exception:
            raise ValidationError('EMAIL ERROR')

    @validator('acc_pass')
    def check_acc_pass(cls, acc_pass):
        try:
            ln = len(acc_pass)
            if ln >= 4 or ln <= 40:
                return acc_pass
            raise ValidationError('PASSWORD ERROR')
        except Exception:
            raise ValidationError('PASSWORD ERROR')