from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy import select
from settings import settings
from .models import UserValuesOrm, Base


class Database:
    def __init__(self):
        self._engine = create_async_engine(
            url=settings.DATABASE_URL_asyncpg,
            echo=False,
            poolclass=AsyncAdaptedQueuePool
        )
        self._async_session_factory = async_sessionmaker(self._engine)

    async def create_table(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_data(self, user_id: int, value: str):
        async with self._async_session_factory() as session:
            # Checking for the existence of an entry with the same user_id and value
            existing_data = await session.execute(
                select(UserValuesOrm).where(UserValuesOrm.user_id == user_id, UserValuesOrm.value == value)
            )
            if existing_data.scalars().first() is None:  # Does such data already exist?
                new_data = UserValuesOrm(user_id=user_id, value=value)
                session.add(new_data)
                await session.commit()
