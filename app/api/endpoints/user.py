from fastapi import APIRouter, HTTPException

from app import schemas
from app.core.constants import NOT_DELETE_USERS_MSG
from app.core.user import auth_backend, fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    raise HTTPException(
        status_code=405,
        detail=NOT_DELETE_USERS_MSG
    )
