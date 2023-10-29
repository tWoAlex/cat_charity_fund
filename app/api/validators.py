from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_exist(
        project_id: int, session: AsyncSession) -> CharityProject:
    project = await charity_project_crud.get_by_id(project_id, session)
    if project is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Проект не найден.')
    return project


def check_charity_project_updatable(
        project: CharityProject, new_data: CharityProjectUpdate) -> None:
    if new_data.full_amount < project.invested_amount:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='В проект уже внесена большая сумма.')
    if project.fully_invested:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Сбор завершён, изменить его нельзя')


def check_charity_project_deletable(project: CharityProject) -> None:
    if project.invested_amount:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='В проект внесены средства, удалить его нельзя.')
