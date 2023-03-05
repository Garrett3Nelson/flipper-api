from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update

from . import models, schemas
from datetime import datetime


async def round_to_nearest(timestamp, timestep):
    dt = datetime.utcfromtimestamp(timestamp)
    rounded_minute = (dt.minute // timestep) * timestep
    dt_rounded = dt.replace(minute=rounded_minute, second=0, microsecond=0)

    return dt_rounded


async def create_item(db: AsyncSession, item: schemas.ItemCreate) -> models.Items:
    db_item = models.Items(**item.dict())
    db.add(db_item)
    await db.commit()
    return db_item


async def get_item(db: AsyncSession, item_id: int) -> models.Items:
    result = await db.get(models.Items, item_id)
    return result


# Write get_items() to pull all items, with limit and filters
async def get_items(db: AsyncSession, limit: int = 100) -> list[models.Items]:
    stmt = select(models.Items).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# Write functions to get full items (with all loaded relationships)
async def get_items_full(db: AsyncSession, limit: int = 100) -> list[models.Items]:
    stmt = select(models.Items).limit(limit).options(
        selectinload(models.Items.categories), selectinload(models.Items.latest),
        selectinload(models.Items.average), selectinload(models.Items.daily),
        selectinload(models.Items.production), selectinload(models.Items.materials)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_item_full(db: AsyncSession, item_id) -> models.Items:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(
        selectinload(models.Items.categories), selectinload(models.Items.latest),
        selectinload(models.Items.average), selectinload(models.Items.daily),
        selectinload(models.Items.production), selectinload(models.Items.materials)
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_item(db: AsyncSession, item: schemas.ItemCreate) -> None:
    stmt = update(models.Items).where(models.Items.id == item.id).values(**item.dict())
    await db.execute(stmt)


async def delete_item(db: AsyncSession, item_id: int) -> None:
    result = await db.get(models.Items, item_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_category(db: AsyncSession, cat: schemas.CategoryCreate) -> models.Category:
    db_cat = models.Category(**cat.dict())
    db.add(db_cat)
    await db.commit()
    await db.refresh(db_cat)
    return db_cat


async def get_category(db: AsyncSession, cat_id: int) -> models.Category:
    result = await db.get(models.Category, cat_id)
    return result


async def get_category_by_item(db: AsyncSession, item_id: int) -> list[models.Category]:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.categories))
    result = await db.execute(stmt)
    return result.scalars().first().categories


async def delete_category(db: AsyncSession, cat_id: int) -> None:
    result = await db.get(models.Category, cat_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_latest(db: AsyncSession, latest: schemas.LatestCreate) -> models.Latest:
    latest.time_stamp = await round_to_nearest(latest.time_stamp, 1)
    db_add = models.Latest(**latest.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_latest(db: AsyncSession, latest_id: int) -> models.Latest:
    result = await db.get(models.Latest, latest_id)
    return result


async def get_latest_all(db: AsyncSession, limit: int = 100) -> list[models.Latest]:
    stmt = select(models.Latest).distinct(models.Latest.item_id).order_by(models.Latest.time_stamp.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_latest_by_item(db: AsyncSession, item_id: int) -> list[models.Latest]:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.latest))
    result = await db.execute(stmt)
    return result.scalars().first().latest


async def delete_latest(db: AsyncSession, latest_id: int) -> None:
    result = await db.get(models.Latest, latest_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_average(db: AsyncSession, average: schemas.AverageCreate) -> models.Average:
    average.time_stamp = await round_to_nearest(average.time_stamp, 1)
    db_add = models.Average(**average.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_average(db: AsyncSession, average_id: int) -> models.Average:
    result = await db.get(models.Average, average_id)
    return result


async def get_average_by_item(db: AsyncSession, item_id: int) -> list[schemas.Average]:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.average))
    result = await db.execute(stmt)
    return result.scalars().first().average


async def delete_average(db: AsyncSession, average_id: int) -> None:
    result = await db.get(models.Average, average_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_daily(db: AsyncSession, daily: schemas.DailyCreate) -> models.Daily:
    db_add = models.Daily(**daily.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_daily(db: AsyncSession, daily_id: int) -> models.Daily:
    result = await db.get(models.Daily, daily_id)
    return result


async def get_daily_by_item(db: AsyncSession, item_id: int) -> list[schemas.Daily]:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.daily))
    result = await db.execute(stmt)
    return result.scalars().first().daily


async def delete_daily(db: AsyncSession, daily_id: int) -> None:
    result = await db.get(models.Daily, daily_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_production(db: AsyncSession, prod: schemas.ProductionCreate) -> models.Production:
    db_add = models.Production(**prod.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_production_full(db: AsyncSession, production_id: int) -> models.Production:
    stmt = select(models.Production).filter(models.Production.id == production_id).options(selectinload(
        models.Production.skills), selectinload(models.Production.materials))

    result = await db.execute(stmt)
    return result.scalars().first()


async def get_production(db: AsyncSession, production_id: int) -> models.Production:
    result = await db.get(models.Production, production_id)
    return result


async def get_production_by_item(db: AsyncSession, item_id: int) -> list[schemas.Production]:
    stmt = select(models.Items).filter(models.Items.id == item_id).options(selectinload(models.Items.production))
    result = await db.execute(stmt)
    return result.scalars().first().production


async def delete_production(db: AsyncSession, production_id: int) -> None:
    result = await db.get(models.Production, production_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_skill(db: AsyncSession, skill: schemas.SkillCreate) -> models.Skill:
    db_add = models.Skill(**skill.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_skill(db: AsyncSession, skill_id: int) -> models.Skill:
    result = await db.get(models.Skill, skill_id)
    return result


async def get_skill_by_production(db: AsyncSession, production_id: int) -> list[models.Skill]:
    stmt = select(models.Production).filter(models.Production.id == production_id).options(selectinload(
        models.Production.skills))
    result = await db.execute(stmt)
    return result.scalars().first().skills


async def delete_skill(db: AsyncSession, skill_id: int) -> None:
    result = await db.get(models.Skill, skill_id)

    if result is not None:
        await db.delete(result)
        await db.commit()


async def create_material(db: AsyncSession, material: schemas.MaterialCreate) -> models.Material:
    db_add = models.Material(**material.dict())
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def get_material(db: AsyncSession, material_id: int) -> models.Material:
    result = await db.get(models.Material, material_id)
    return result


async def get_material_by_production(db: AsyncSession, production_id: int) -> models.Material:
    stmt = select(models.Production).filter(models.Production.id == production_id).options(selectinload(
        models.Production.materials))
    result = await db.execute(stmt)
    return result.scalars().first().materials


async def delete_material(db: AsyncSession, material_id: int) -> None:
    result = await db.get(models.Material, material_id)

    if result is not None:
        await db.delete(result)
        await db.commit()
