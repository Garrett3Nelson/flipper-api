from fastapi import Depends, FastAPI, HTTPException
from .sql import crud, models, schemas

app = FastAPI()


@app.get('/')
async def home_page():
    pass
