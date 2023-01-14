from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update

from . import models, schemas


async def create_item(db: AsyncSession, item: schemas.ItemCreate):
    db_item = models.Items(**item.dict())
    db.add(db_item)
    await db.commit()
    return db_item


async def get_item(db: AsyncSession, item_id: int):
    result = await db.get(models.Items, item_id)
    return result


async def update_item(db: AsyncSession, item: schemas.ItemCreate):
    stmt = update(models.Items).where(models.Items.id == item.id).values(**item.dict())
    await db.execute(stmt)


async def delete_item(db: AsyncSession, item_id: int):
    result = await db.get(models.Items, item_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_category(db: AsyncSession, cat: schemas.CategoryCreate):
    db_cat = models.Category(**cat.dict())
    db.add(db_cat)
    await db.commit()
    await db.refresh(db_cat)
    return db_cat


async def get_category(db: AsyncSession, cat_id: int):
    result = await db.get(models.Category, cat_id)
    return result


async def get_category_by_item(db: AsyncSession, item_id: int):
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.categories))
    result = await db.execute(stmt)
    return result.scalars().first().categories


async def delete_category(db: AsyncSession, cat_id: int):
    result = await db.get(models.Category, cat_id)

    if result is not None:
        await db.delete(result)
        await db.commit()
