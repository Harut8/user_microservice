from abc import abstractmethod, ABCMeta
from typing import Union
from models.user_model.user_model import UserInfo, AccountRegModel


class UserServiceInterface(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    async def get_user_from_db(*, username) -> Union[UserInfo, None]:
        ...

    @staticmethod
    @abstractmethod
    async def post_acc_into_temp_db(add_user_data: AccountRegModel) -> Union[bool, None]:
        ...
