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


@app.get('/item/', response_model=schemas.Item)
async def read_items():
    async with async_session() as session:
        async with session.begin():
            return crud.get_item(session, item_id=1)
