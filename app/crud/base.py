from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
        all_objects = await session.scalars(select(self.model))
        return all_objects.all()

    async def create(self, obj_in, session: AsyncSession):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        # await session.refresh(db_obj)
        return db_obj
