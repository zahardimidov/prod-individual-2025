from infra.config import settings
from infra.database.models import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(url=settings.ENGINE, echo=False)
async_session = async_sessionmaker(engine)


async def run_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def text_query(query: str):
    async with async_session() as session:
        await session.execute(text(query))
        await session.commit()
