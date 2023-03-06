from fastapi import Depends, FastAPI, HTTPException

from sql import crud, models, schemas
from sql.database import async_session, engine

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.post('/latest/', response_model=schemas.Latest)
async def create_latest(latest: schemas.LatestCreate):
    async with async_session() as session:
        return await crud.create_latest(session, latest=latest)


@app.get('/latest/', response_model=list[schemas.Latest])
async def read_latest(limit: int = 100):
    async with async_session() as session:
        return await crud.get_latest_all(session, limit=limit)


@app.get('/latest/{item_id}/', response_model=schemas.Latest)
async def read_latest_by_item(item_id: int):
    async with async_session() as session:
        return await crud.get_latest_by_item(session, item_id=item_id)


@app.post('/average/', response_model=schemas.Average)
async def create_average(average: schemas.AverageCreate):
    async with async_session() as session:
        return await crud.create_average(session, average=average)


@app.get('/average/', response_model=list[schemas.Average])
async def read_average(limit: int = 100):
    async with async_session() as session:
        return await crud.get_average_all(session, limit=limit)


@app.get('/average/{item_id}/', response_model=schemas.Average)
async def read_average_by_item(item_id: int):
    async with async_session() as session:
        return await crud.get_average_by_item(session, item_id=item_id)


@app.post('/daily/', response_model=schemas.Daily)
async def create_average(daily: schemas.DailyCreate):
    async with async_session() as session:
        return await crud.create_daily(session, daily=daily)


@app.get('/daily/', response_model=list[schemas.Daily])
async def read_average(limit: int = 100):
    async with async_session() as session:
        return await crud.get_daily_all(session, limit=limit)


@app.get('/daily/{item_id}/', response_model=schemas.Daily)
async def read_average_by_item(item_id: int):
    async with async_session() as session:
        return await crud.get_daily_by_item(session, item_id=item_id)


@app.get('/items/full/', response_model=list[schemas.ItemFull])
async def read_items_full(limit: int = 100):
    async with async_session() as session:
        return await crud.get_items_full(session, limit=limit)


@app.get('/items/full/{item_id}/', response_model=schemas.ItemFull)
async def read_item_full(item_id: int):
    async with async_session() as session:
        return await crud.get_item_full(session, item_id=item_id)


@app.post('/items/', response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate):
    async with async_session() as session:
        return await crud.create_item(session, item=item)


@app.get('/items/', response_model=list[schemas.Item])
async def read_items(limit: int = 100):
    async with async_session() as session:
        return await crud.get_items(session, limit=limit)


@app.get('/items/{item_id}/', response_model=schemas.Item)
async def read_item(item_id: int):
    async with async_session() as session:
        return await crud.get_item(session, item_id=item_id)
