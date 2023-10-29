from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseTransaction, CharityProject, Donation


def cover_project(project: CharityProject):
    project.invested_amount = project.full_amount
    project.fully_invested = True


def cover_donation(donation: Donation):
    donation.invested_amount = donation.full_amount
    donation.fully_invested = True


async def uncovered_transactions(
        session: AsyncSession) -> (list[CharityProject], list[Donation]):
    projects_select_statement = select(CharityProject).where(
        CharityProject.fully_invested != True) # noqa
    donations_select_statement = select(Donation).where(
        Donation.fully_invested != True) # noqa

    projects = await session.scalars(projects_select_statement)
    donations = await session.scalars(donations_select_statement)
    return projects.all(), donations.all()


def mutual_coverage(projects: list[CharityProject],
                    donations: list[Donation]):
    projects_index, donations_index = 0, 0
    while (projects_index < len(projects) and
           donations_index < len(donations)):
        project: CharityProject = projects[projects_index]
        deficit = project.full_amount - project.invested_amount

        if not deficit:
            cover_project(project)
            projects_index += 1
            continue

        donation: Donation = donations[donations_index]
        investable = donation.full_amount - donation.invested_amount

        if investable > deficit:
            cover_project(project)
            projects_index += 1
            donation.invested_amount += deficit
        elif investable < deficit:
            cover_donation(donation)
            donations_index += 1
            project.invested_amount += investable
        else:
            cover_donation(donation)
            cover_project(project)
            donations_index += 1
            projects_index += 1


async def update_objects(objects_lists: list[BaseTransaction],
                         session: AsyncSession):
    for object_list in objects_lists:
        session.add_all(object_list)
    await session.commit()


async def update_investments(session: AsyncSession):
    projects, donations = await uncovered_transactions(session)
    mutual_coverage(projects, donations)
    await update_objects([projects, donations], session)
