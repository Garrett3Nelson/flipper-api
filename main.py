from fastapi import Depends, FastAPI, HTTPException

from sql import crud, models, schemas
from sql.database import async_session, engine

app = FastAPI()


# # Dependency
# async def get_db():
#     db = async_session()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.on_event("startup")
# async def startup():
#     await engine.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get('/')
async def root():
    return {"message": "Hello World"}


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


@app.get('/items/full/', response_model=list[schemas.ItemFull])
async def read_items_full(limit: int = 100):
    async with async_session() as session:
        return await crud.get_items_full(session, limit=limit)


@app.get('/items/full/{item_id}/', response_model=schemas.ItemFull)
async def read_item_full(item_id: int):
    async with async_session() as session:
        return await crud.get_item_full(session, item_id=item_id)
