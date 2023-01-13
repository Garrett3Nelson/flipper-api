from fastapi import Depends, FastAPI, HTTPException
# from sql import crud, models, schemas
from sql.database import engine

app = FastAPI()


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
