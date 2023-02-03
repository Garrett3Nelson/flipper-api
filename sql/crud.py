from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update

from . import models, schemas


async def create_item(db: AsyncSession, item: schemas.ItemCreate) -> schemas.Item:
    db_item = models.Items(**item.dict())
    db.add(db_item)
    await db.commit()
    return db_item


async def get_item(db: AsyncSession, item_id: int) -> schemas.Item:
    result = await db.get(models.Items, item_id)
    return result


async def update_item(db: AsyncSession, item: schemas.ItemCreate) -> None:
    stmt = update(models.Items).where(models.Items.id == item.id).values(**item.dict())
    await db.execute(stmt)


async def delete_item(db: AsyncSession, item_id: int) -> None:
    result = await db.get(models.Items, item_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_category(db: AsyncSession, cat: schemas.CategoryCreate) -> schemas.Category:
    db_cat = models.Category(**cat.dict())
    db.add(db_cat)
    await db.commit()
    await db.refresh(db_cat)
    return db_cat


async def get_category(db: AsyncSession, cat_id: int) -> schemas.Category:
    result = await db.get(models.Category, cat_id)
    return result


async def get_category_by_item(db: AsyncSession, item_id: int) -> schemas.Category | list[schemas.Category]:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.categories))
    result = await db.execute(stmt)
    return result.scalars().first().categories


async def delete_category(db: AsyncSession, cat_id: int) -> None:
    result = await db.get(models.Category, cat_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_latest(db: AsyncSession, latest: schemas.LatestCreate) -> schemas.Latest:
    db_add = models.Latest(**latest.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_latest(db: AsyncSession, latest_id: int) -> schemas.Latest:
    result = await db.get(models.Latest, latest_id)
    return result


async def get_latest_by_item(db: AsyncSession, item_id: int) -> schemas.Latest:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.latest))
    result = await db.execute(stmt)
    return result.scalars().first().latest


async def delete_latest(db: AsyncSession, latest_id: int) -> None:
    result = await db.get(models.Latest, latest_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_average(db: AsyncSession, average: schemas.AverageCreate) -> schemas.Average:
    db_add = models.Average(**average.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_average(db: AsyncSession, average_id: int) -> schemas.Average:
    result = await db.get(models.Average, average_id)
    return result


async def get_average_by_item(db: AsyncSession, item_id: int) -> schemas.Average:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.average))
    result = await db.execute(stmt)
    return result.scalars().first().average


async def delete_average(db: AsyncSession, average_id: int) -> None:
    result = await db.get(models.Average, average_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_daily(db: AsyncSession, daily: schemas.DailyCreate) -> schemas.Daily:
    db_add = models.Daily(**daily.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_daily(db: AsyncSession, daily_id: int) -> schemas.Daily:
    result = await db.get(models.Daily, daily_id)
    return result


async def get_daily_by_item(db: AsyncSession, item_id: int) -> schemas.Daily:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.daily))
    result = await db.execute(stmt)
    return result.scalars().first().daily


async def delete_daily(db: AsyncSession, daily_id: int) -> None:
    result = await db.get(models.Daily, daily_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_production(db: AsyncSession, latest: schemas.ProductionCreate) -> schemas.Production:
    db_add = models.Production(**latest.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_production_full(db: AsyncSession, production_id: int) -> schemas.Production:
    stmt = select(models.Production).filter(models.Production.id == production_id).options(selectinload(
        models.Production.skills), selectinload(models.Production.materials))

    result = await db.execute(stmt)
    return result.scalars().first()


async def get_production(db: AsyncSession, production_id: int) -> schemas.Production:
    result = await db.get(models.Production, production_id)
    return result


async def get_production_by_item(db: AsyncSession, item_id: int) -> schemas.Production:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.production))
    result = await db.execute(stmt)
    return result.scalars().first().production


async def delete_production(db: AsyncSession, production_id: int) -> None:
    result = await db.get(models.Production, production_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_skill(db: AsyncSession, latest: schemas.SkillCreate) -> schemas.Skill:
    db_add = models.Skill(**latest.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_skill(db: AsyncSession, skill_id: int) -> schemas.Skill:
    result = await db.get(models.Skill, skill_id)
    return result


async def get_skill_by_production(db: AsyncSession, production_id: int) -> schemas.Skill:
    stmt = select(models.Production).filter(models.Production.id == production_id).options(selectinload(
        models.Production.skills))
    result = await db.execute(stmt)
    return result.scalars().first().skills


async def delete_skill(db: AsyncSession, skill_id: int) -> None:
    result = await db.get(models.Skill, skill_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_material(db: AsyncSession, latest: schemas.MaterialCreate) -> schemas.Material:
    db_add = models.Material(**latest.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_material(db: AsyncSession, material_id: int) -> schemas.Material:
    result = await db.get(models.Material, material_id)
    return result


async def get_material_by_production(db: AsyncSession, production_id: int) -> schemas.Material | list[schemas.Material]:
    stmt = select(models.Production).filter(models.Production.id == production_id).options(selectinload(
        models.Production.materials))
    result = await db.execute(stmt)
    return result.scalars().first().materials


async def delete_material(db: AsyncSession, material_id: int) -> None:
    result = await db.get(models.Material, material_id)

    if result is not None:
        await db.delete(result)
        await db.commit()
