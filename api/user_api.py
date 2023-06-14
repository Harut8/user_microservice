from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from service.user_service_manager.user_service_manager import UserServiceManager
from starlette import status
from starlette.responses import RedirectResponse
from models.user_model.user_model import AccountRegModel,\
    Language,\
    AccRecoveryEmail,\
    AccountVerifyModel,\
    AccountRecModel,\
    Refresh
from auth.auth import \
    get_current_user,\
    verify_password,\
    check_refresh_token,\
    create_access_token,\
    create_refresh_token


user_router = APIRouter(tags=["USER API"], prefix="/user")


@user_router.get('/ping')
async def user_ping():
    return {"status": "USER PINGING"}


@user_router.post("/signin")
async def user_login(user_info: OAuth2PasswordRequestForm = Depends()):
    user = await UserServiceManager.get_user_from_db(username=user_info.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.c_pass
    if not verify_password(user_info.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.c_id),
        "refresh_token": create_refresh_token(user.c_id),
    }


@user_router.post("/signup")
async def user_signup(add_user_data: AccountRegModel):
    if await UserServiceManager.post_acc_into_temp_db(add_user_data):
        return {"status": "success"}
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect data"
        )


@user_router.post('/recovery/mail')
async def recovery_send_mail(receiver_info: AccRecoveryEmail):
    _is_send = await UserServiceManager.send_recovery_code(receiver_info.receiver_email)
    if _is_send:
        return {"status": "success"}
    raise HTTPException(400, detail='ERROR')


@user_router.post('/recovery')
async def recovery_pass(new_info: AccountRecModel):
    _update_status = await UserServiceManager.update_password(
        new_info.acc_email,
        new_info.acc_new_pass
    )
    if _update_status:
        return {"status": "success"}
    raise HTTPException(400, detail='ERROR')


@user_router.post('/recovery/check')
async def recovery_check(check_info: AccountVerifyModel):
    _check_state = await UserServiceManager.check_recovery_code(
        check_info.receiver_email,
        check_info.code_for_verify)
    if _check_state:
        return {"status": "success"}
    raise HTTPException(400, detail='ERROR')


@user_router.get('/verify-email')
async def verify_registration_with_email(token_verify: str, data: str):
    _verify_state = await UserServiceManager.verify_registration_with_email(token_verify)
    print(_verify_state)
    if _verify_state:
        redirect_page = RedirectResponse("https://pcassa.ru/")
        return redirect_page
    elif _verify_state == -1:
        return {"status": "EMPTY USER ID"}
    elif _verify_state == -2:
        return {"status": "WRONG VERIFY ID"}
    else:
        return {"status": "Redirect error"}


@user_router.get("/me")
async def get_user_friends(language: Language,  current_user=Depends(get_current_user)):
    _user_and_tarif = await UserServiceManager.get_user_info(language.value, current_user.c_id)
    if _user_and_tarif:
        return _user_and_tarif
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect data"
    )


@user_router.get("/get-user")
async def get_user(user=Depends(get_current_user)):
    return user


@user_router.post('/refresh-token')
async def refresh_token(refresh: Refresh, user=Depends(get_current_user)):
    _refresh_check = await check_refresh_token(refresh.refresh_token)
    if _refresh_check:
        return {
            "access_token": create_access_token(user.c_id),
            "refresh_token": create_refresh_token(user.c_id),
        }
    raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN UPDATE ERROR'})


@user_router.get('/links')
async def get_app_links():
    _app_links = await UserServiceManager.get_app_links()
    if _app_links:
        return _app_links
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect data"
    )

