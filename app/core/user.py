from typing import Optional, Union
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager,
                           FastAPIUsers,
                           IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport,
                                          JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy)


class UserManager(IntegerIDMixin, BaseUserManager[User, UUID]):
    async def validate_password(self,
                                password: str,
                                user: Union[UserCreate, User]) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters')
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail')

    async def on_after_register(self,
                                user: User,
                                request: Optional[Request] = None) -> None:
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi__users = FastAPIUsers[User, UUID](
    get_user_manager, (auth_backend,))


current_user = fastapi__users.current_user(active=True)
current_superuser = fastapi__users.current_user(active=True, superuser=True)
