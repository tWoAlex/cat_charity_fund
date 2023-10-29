from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDBFull, DonationDBShort
from app.services.investments import update_investments


router = APIRouter()


@router.get('/', name='Список всех пожертвований',
            response_model=list[DonationDBFull],
            response_model_exclude_none=True,
            dependencies=(Depends(current_superuser),))
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_all(session)


@router.post('/', name='Сделать пожертвование',
             response_model=DonationDBShort,
             response_model_exclude_none=True)
async def donate(donation: DonationCreate,
                 session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_user)):
    donation = await donation_crud.create(donation, session, user)
    await update_investments(session)
    await session.refresh(donation)
    return donation


@router.get('/my', name='Ваши пожертвования',
            response_model=list[DonationDBShort],
            response_model_exclude_none=True)
async def get_my_donations(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    return await donation_crud.get_users_donations(session, user)
