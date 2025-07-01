from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta

from .schemas import UserCreateModel, UserLoginModel
from .service import UserService
from ...auth.models import User
from .utils import create_access_token, verify_password
from src.db.core import get_session
from ..config import settings
# from src.db.redis import add_jti_to_blocklist
from ...auth.dependecies import AccessTokenBearer

auth_router = APIRouter()

user_service = UserService()

@auth_router.post(
    "/register", response_model=User, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email.lower()
    user_data.email = email

    if await user_service.user_exists(email, session):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists.",
        )

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email.lower()
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)}
    )

    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)},
        refresh=True,
        expiry=timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS),
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_verified": user.is_verified
            },
        },
    )


@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    jti = token_details['jti']

    # await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )