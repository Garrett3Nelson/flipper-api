import asyncio

from sql.database import async_session, engine, Base
from sql import models, schemas


# With a fresh database, run this command before pytest will work.
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# async def create_data():
#     async with async_session() as session:
#         item = schemas.ItemCreate(id=2, name="Cannonball", market=1000, limit=5000, members=True, high_alch=10,
#                                   low_alch=5)
#         cat = schemas.CategoryCreate(name='Test', item_id=2)
#         await crud.create_item(session, item)
#         await crud.create_category(session, cat)


if __name__ == '__main__':
    asyncio.run(create_tables())
    # asyncio.run(create_data())
