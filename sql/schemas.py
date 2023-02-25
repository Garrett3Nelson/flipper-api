from pydantic import BaseModel
from datetime import datetime, date


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


class LatestBase(BaseModel):
    item_id: int
    low_price: int
    high_price: int
    time_stamp: datetime


class LatestCreate(LatestBase):
    pass


class Latest(LatestBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class AverageBase(BaseModel):
    item_id: int
    low_price: int
    high_price: int
    low_volume: int
    high_volume: int
    time_stamp: datetime


class AverageCreate(AverageBase):
    pass


class Average(AverageBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class DailyBase(BaseModel):
    item_id: int
    price: int
    volume: int


class DailyCreate(DailyBase):
    pass


class Daily(DailyBase):
    id: int
    date_stamp: date
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class MaterialBase(BaseModel):
    production_id: int
    name: str
    quantity: int


class MaterialCreate(MaterialBase):
    pass


class Material(MaterialBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    production_id: int
    experience: float
    level: int
    name: str
    boostable: bool


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class ProductionBase(BaseModel):
    item_id: int
    ticks: int
    facilities: str | None
    members: str
    cost: int
    quantity: int


class ProductionCreate(ProductionBase):
    pass


class Production(ProductionBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class ProductionFull(Production):
    materials: list[Material] = []
    skills: list[Skill] = []


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

    class Config:
        orm_mode = True


class ItemFull(Item):
    categories: list[Category] = []
    latest: list[Latest] = []
    average: list[Average] = []
    daily: list[Daily] = []
    production: list[Production] = []
    materials: list[Material] = []
