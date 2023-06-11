from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from service.user_service_manager.user_service_manager import UserServiceManager
from starlette import status
from models.user_model.user_model import AccountRegModel
from auth.auth import \
    get_current_user,\
    verify_password,\
    get_hashed_password,\
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


@user_router.get('/verify-email')
async def verify_registration_with_email(token_verify: str, data: str):
    print(token_verify)


@user_router.get("/friends")
async def get_user_friends(current_username=Depends(get_current_user)):
    print(current_username)

