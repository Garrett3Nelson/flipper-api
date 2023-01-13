from pydantic import BaseModel
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    item_id: int


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    id: int
    name: str
    market: int
    limit: int
    members: bool
    high_alch: int
    low_alch: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    created: datetime
    updated: datetime

    categories: list[Category] = []

    class Config:
        orm_mode = True
