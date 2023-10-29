from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_by_id(self, project_id: int, session: AsyncSession):
        return await session.get(CharityProject, project_id)

    async def get_by_name(self, project_name: str, session: AsyncSession):
        return await session.scalar(
            select(CharityProject).where(CharityProject.name == project_name))

    async def update(self, db_ojb, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_ojb)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_ojb, field, update_data[field])
        session.add(db_ojb)
        await session.commit()
        return db_ojb

    async def delete(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)
