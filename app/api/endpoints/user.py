from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi__users
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter()


router.include_router(
    fastapi__users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)
router.include_router(
    fastapi__users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)
router.include_router(
    fastapi__users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users']
)


@router.delete('/users/{id}', tags=['users'], deprecated=True)
def delete_user(id: UUID):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                        detail=('Удаление пользователей запрещено. '
                                'При необходимости деактивируйте'))
