from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.database import db_settings
from src.repositories.reports import ReportRepository

async_engine = create_async_engine(url=db_settings.url)


async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


class SessionManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session: AsyncSession = session_factory()

        # репозитории
        self.reports = ReportRepository(self.session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, *args):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_db():
    async with SessionManager(async_session_factory) as db:
        yield db
