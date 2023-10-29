from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exist,
                                check_charity_project_deletable,
                                check_charity_project_same_name,
                                check_charity_project_updatable)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import update_investments


router = APIRouter()


@router.get('/', name='Список всех проектов',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_all(session)


@router.post('/', name='Создать проект',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=(Depends(current_superuser),))
async def create_project(project_in: CharityProjectCreate,
                         session: AsyncSession = Depends(get_async_session)):
    await check_charity_project_same_name(project_in.name, session)
    project = await charity_project_crud.create(project_in, session)
    await update_investments(session)
    await session.refresh(project)
    return project


@router.patch('/{project_id}', name='Обновить проект',
              response_model=CharityProjectDB,
              dependencies=(Depends(current_superuser),))
async def update_project(project_id: int,
                         project_in: CharityProjectUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    db_project = await check_charity_project_exist(project_id, session)
    await check_charity_project_updatable(db_project, project_in, session)
    db_project = await charity_project_crud.update(db_project, project_in, session)
    await update_investments(session)
    await session.refresh(db_project)
    return db_project


@router.delete('/{project_id}', name='Удалить проект',
               response_model=CharityProjectDB,
               dependencies=(Depends(current_superuser),))
async def delete_project(project_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    db_project = await check_charity_project_exist(project_id, session)
    check_charity_project_deletable(db_project)
    return await charity_project_crud.delete(db_project, session)
