import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.environ['DB_URL']

engine = create_async_engine(DB_URL, echo=True, future=True)
Base = declarative_base()

async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
