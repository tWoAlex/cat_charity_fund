from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def create(self, obj_in, session: AsyncSession, user: User):
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        # await session.refresh(db_obj)
        return db_obj

    async def get_users_donations(self, session: AsyncSession, user: User):
        donations = await session.scalars(
            select(Donation).where(Donation.user_id == user.id))
        return donations.all()


donation_crud = CRUDDonation(Donation)
