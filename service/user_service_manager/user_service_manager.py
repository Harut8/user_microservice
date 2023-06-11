import os
import sys
from uuid import UUID
from repository.user_db_manager.user_db_manager import UserDbManager
from models.user_model.user_model import UserInfo, AccountRegModel
from typing import Union
from service.user_service_manager.user_service_interface import UserServiceInterface
from service.url_token_generators.token_creator import create_token_for_email_verify, generate_url_for_email_verify
from mailing.verify_mailing.send_account_verify_link import send_email_verify_link
from amqp_service.celery_app.celery_app import celery_decor

class UserServiceManager(UserServiceInterface):

    @staticmethod
    async def get_user_from_db(*, username) -> Union[UserInfo, None]:
        try:
            user_info = await UserDbManager.get_user_from_db(username=username)
            if user_info:
                return UserInfo(**user_info)
            return
        except Exception as e:
            raise e

    @staticmethod
    async def post_acc_into_temp_db(add_user_data: AccountRegModel) -> Union[bool, None]:
        try:
            _user_add_state = await UserDbManager.post_acc_into_temp_db(item=add_user_data)
            if _user_add_state:
                id_for_link: Union[str, UUID] = _user_add_state["temp_id"]
                id_for_link_generated_JWTEncoded = create_token_for_email_verify(str(id_for_link))
                generated_link = generate_url_for_email_verify(id_=id_for_link_generated_JWTEncoded)
                send_email_verify_link.delay(_user_add_state["temp_email"], generated_link)
                return True
            return
        except Exception as e:
            raise e
