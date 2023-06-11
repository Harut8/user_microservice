import uuid
from abc import abstractmethod, ABCMeta
from typing import Union
from asyncpg import Record

from models.user_model.user_model import AccountRegModel


class UserDbInterface(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    async def get_user_from_db(username) -> Record:
        ...

    @staticmethod
    @abstractmethod
    async def post_acc_into_temp_db(*, item: AccountRegModel) -> Union[dict[str, uuid.UUID], None]:
        ...


