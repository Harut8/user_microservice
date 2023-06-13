import uuid
from typing import Union

from auth.auth import get_hashed_password
from models.user_model.user_model import AccountRegModel
from repository.core.core import DbConnection, fetch_row_transaction, insert_row_transaction, fetch_transaction, \
    execute_delete_query
from dataclasses import dataclass
from repository.user_db_manager.user_db_interface import UserDbInterface
from asyncpg import Record


@dataclass
class UserDbManager(UserDbInterface):

    @staticmethod
    async def get_user_from_db(*, username) -> Record:
        _user_info = await fetch_row_transaction(
            """select c_id, c_pass, c_email from company where c_email = $1""",
            username)
        return _user_info

    @staticmethod
    async def get_user_from_db_by_uuid(uuid):
        _user_info = await fetch_row_transaction(
            """select c_id, c_email from company where c_id = $1""",
            uuid)
        return _user_info

    @staticmethod
    async def post_acc_into_temp_db(*, item: AccountRegModel) -> Union[dict[str, uuid.UUID | str], None, bool]:
        """ INSERT acc INFO INTO TEMP DATABASE"""
        try:
            #  get from registered users where username and phone number
            _check_acc_in_temp = await fetch_row_transaction(
                """ SELECT c_name, c_email, c_phone FROM company
                    WHERE c_name = $1
                    or 
                    c_email = $2
                    or 
                    c_phone = $3
                """,
                item.acc_org_name,
                item.acc_email,
                item.acc_phone
            )
            if _check_acc_in_temp:  # there is a company with these parameters
                return False

            hash_pass = get_hashed_password(item.acc_pass)
            await execute_delete_query(
                """DELETE FROM temp_company
                   WHERE t_c_name = $1 
                   or t_c_email = $2 
                   or t_c_phone = $3""",
                item.acc_org_name,
                item.acc_email,
                item.acc_phone)
            _temp_id = await fetch_row_transaction(f"""
                INSERT
            INTO
            temp_company(
                t_c_name,
                t_c_country,
                t_c_pass,
                t_c_contact_name,
                t_c_phone,
                t_c_email,
                t_c_verify_link,
                t_c_inn,
                t_c_kpp,
                t_c_k_schet,
                t_c_r_schet,
                t_c_bik,
                t_c_bank_name,
                t_c_address)
            VALUES(
                $1,
                $2,
                '{hash_pass}',
                $3,
                $4,
                $5,
                'link',
                $6,
                $7,
                $8,
                $9,
                $10,
                $11,
                $12) RETURNING t_id""",
                                         item.acc_org_name,
                                         str(item.acc_country),
                                         item.acc_contact_name,
                                         item.acc_phone,
                                         item.acc_email,
                                         item.acc_inn,
                                         item.acc_kpp,
                                         item.acc_k_schet,
                                         item.acc_r_schet,
                                         item.acc_bik,
                                         item.acc_bank_name,
                                         item.acc_address,
                                         )
            return {'temp_id': _temp_id, 'temp_email': item.acc_email}
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def verify_registration_with_email(*, temp_id):
        try:
            _verify_state = await fetch_row_transaction(
                """SELECT del_tmp_add_company($1)""",
                temp_id
            )
            return _verify_state
        except Exception as e:
            print(e)
            return
    @staticmethod
    async def get_user_info(language, user_uuid):
        _user_info = await fetch_row_transaction(
            """
            SELECT  c_id,
                    c_unique_id,
                    c_name,
                    c_contact_name,
                    c_phone,
                    c_email
            FROM company
            WHERE c_id = $1
            """, user_uuid)
        _user_info = {
            'c_id': _user_info['c_id'],
            'c_unique_id': _user_info['c_unique_id'],
            'c_name': _user_info['c_name'],
            'c_contact_name': _user_info['c_contact_name'],
            'c_phone': _user_info['c_phone'],
            'c_email': _user_info['c_email'],
        }
        _tariff_info = await fetch_transaction(
            """
            SELECT 
                      distinct t_id,
                      t_name[$2],
                      end_license::date,
                      true as order_state
                FROM tarif 
                join client_tarif ct on ct.c_t_id = $1 and ct.c_t_tarif_id  = t_id
                where t_id in (select tarif_id_fk from saved_order_and_tarif soat where company_id = $1
                and for_view=true)
                union all
                SELECT 
                      distinct t_id,
                      t_name[$2],
                      null::date,
                      false as order_state
                FROM tarif 
                where t_id in (select tarif_id_fk from saved_order_and_tarif soat where company_id = $1
                and for_view=true
                except select c_t_tarif_id  from client_tarif ct2  where c_t_id  = $1)""",
            user_uuid,
            language
        )
        data = _user_info | {"tarif_list": _tariff_info}
        print(data)
        return data

    @staticmethod
    async def get_app_links():
        _links = await fetch_transaction(
            """SELECT * FROM links order by product_id"""
        )
        return _links