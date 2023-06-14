from auth.auth import decode_token
from uuid import UUID
from repository.user_db_manager.user_db_manager import UserDbManager
from models.user_model.user_model import UserInfo, AccountRegModel, AccountViewModel
from typing import Union

from service.redis_client.redis_client import RedisClient
from service.user_service_manager.user_service_interface import UserServiceInterface
from service.url_token_generators.token_creator import create_token_for_email_verify, generate_url_for_email_verify
from mailing.verify_mailing.send_account_verify_link import send_email_verify_link
from mailing.verify_mailing.send_account_recovery_code import send_account_recovery_code
from asyncpg import Record


language_dict = {
        "ru": 1,
        "en": 2,
        "hy": 3
    }


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
                id_for_link: Union[str, UUID, Record] = _user_add_state["temp_id"]
                id_for_link = str(id_for_link["t_id"])
                id_for_link_generated_JWTEncoded = create_token_for_email_verify(id_for_link)
                generated_link = generate_url_for_email_verify(id_=id_for_link_generated_JWTEncoded)
                send_email_verify_link.delay(_user_add_state["temp_email"], generated_link)
                return True
            return
        except Exception as e:
            raise e

    @staticmethod
    async def verify_registration_with_email(token_verify):
        """
        -1 EMPTY USER ID
        -2 WRONG VERIFY ID
        :param token_verify:
        :return:
        """
        try:
            temp_payload = await decode_token(token_verify)
            temp_id = temp_payload['sub']
            if not temp_id:
                return -1
            _verify_state = await UserDbManager.verify_registration_with_email(temp_id=temp_id)
            if not _verify_state:
                return -2
            _info = _verify_state["del_tmp_add_company"]
            _unique_id = _info["c_unique_id"]
            _c_email = _info["c_email"]
            return True
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def get_user_info(language, user_uuid):
        try:
            _user_info = await UserDbManager.get_user_info(language_dict[language],user_uuid)
            if _user_info is not None:
                return AccountViewModel(
                    c_id=_user_info["c_id"],
                    c_unique_id=_user_info["c_unique_id"],
                    c_name=_user_info["c_name"],
                    c_contact_name=_user_info["c_contact_name"],
                    c_phone=_user_info["c_phone"],
                    c_email=_user_info["c_email"],
                    tarif_list=_user_info["tarif_list"],
                )
            return
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def get_app_links():
        try:
            __app = ("cass_stantion_name",
                 "mobile_cass_name",
                 "web_manager_name",
                 "mobile_manager_name",
                 )

            _links = await UserDbManager.get_app_links()
            if _links is not None:
                return {i: j["product_link"] for i, j in zip(__app, _links)}
            return
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def send_recovery_code(receiver_info):
        try:
            import random
            _message = "".join([str(random.randint(0, 9)) for i in range(9)])
            if RedisClient.set_var(receiver_info, _message, 600):
                send_account_recovery_code.delay(receiver_email=receiver_info, message=_message)
                return True
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def check_recovery_code(receiver_email, verify_code):
        try:
            _code = RedisClient.get_var(receiver_email).decode('utf-8')
            if _code == str(verify_code):
                return True
            return
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def update_password(_email, _password):
        try:
            from auth.auth import get_hashed_password
            _password = get_hashed_password(_password)
            _state = await UserDbManager.update_password(_email, _password)
            if not _state:
                return
            return True
        except Exception as e:
            print(e)
            return
