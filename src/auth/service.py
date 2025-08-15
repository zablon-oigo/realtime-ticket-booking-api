from ...auth.models import User
from ...auth.schemas import UserCreateModel
from .utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


class UserService:
    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def user_exists(email: str, session: AsyncSession) -> bool:
        return await UserService.get_user_by_email(email, session) is not None

    @staticmethod
    async def create_user(user_data: UserCreateModel, session: AsyncSession) -> User:
        if await UserService.user_exists(user_data.email, session):
            raise ValueError(f"User with email '{user_data.email}' already exists.")

        user_data_dict = user_data.model_dump(exclude={"password"})
        hashed_password = generate_password_hash(user_data.password)

        new_user = User(**user_data_dict, password_hash=hashed_password)

        session.add(new_user)

        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError("Failed to create user due to a database constraint.") from e

        await session.refresh(new_user)
        return new_user