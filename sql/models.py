import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Date
from sqlalchemy.orm import relationship
from .database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), unique=True)
    market = Column(Integer)
    limit = Column(Integer)
    members = Column(Boolean)
    high_alch = Column(Integer)
    low_alch = Column(Integer)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    categories = relationship("Category", back_populates='item', cascade="all, delete, delete-orphan")
    latest = relationship("Latest", back_populates='item', cascade="all, delete, delete-orphan")
    average = relationship("Average", back_populates='item', cascade="all, delete, delete-orphan")
    daily = relationship("Daily", back_populates='item', cascade="all, delete, delete-orphan")
    production = relationship("Production", back_populates='item', cascade="all, delete, delete-orphan")
    materials = relationship("Material", back_populates='item', cascade="all, delete, delete-orphan")

    # indices = relationship("TradeIndex", back_populates='item')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name})"


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    name = Column(String(100), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    item = relationship('Items', back_populates='categories')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, item={self.item_id})"


class Latest(Base):
    __tablename__ = "latest"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    low_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    item = relationship('Items', back_populates='latest')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Latest(id={self.id}, item={self.item_id}, low_price={self.low_price}, high_price={self.high_price})"


class Average(Base):
    __tablename__ = "average"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    low_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    low_volume = Column(Integer, nullable=False)
    high_volume = Column(Integer, nullable=False)
    time_stamp = Column(DateTime, nullable=False, unique=True)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    item = relationship('Items', back_populates='average')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Average(id={self.id}, item={self.item_id}, low_price={self.low_price}, high_price={self.high_price}" \
               f", low_volume={self.low_volume}, high_volume={self.high_volume})"


class Daily(Base):
    __tablename__ = "daily"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    date_stamp = Column(Date, nullable=False, default=datetime.date.today(), unique=True)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    item = relationship('Items', back_populates='daily')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Daily(id={self.id}, item={self.item_id}, price={self.price}, volume={self.volume})"


class Production(Base):
    __tablename__ = "production"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    ticks = Column(Integer, nullable=False)
    facilities = Column(String, nullable=False)
    members = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    item = relationship('Items', back_populates='production')
    materials = relationship('Material', back_populates='production')
    skills = relationship('Skill', back_populates='production')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Production(id={self.id}, item={self.item_id}, ticks={self.ticks}, facilities={self.facilities}, " \
               f"materials={self.materials}, skills={self.skills})"


class Material(Base):
    __tablename__ = "material"

    id = Column(Integer, primary_key=True)
    production_id = Column(Integer, ForeignKey('production.id'))
    name = Column(String, ForeignKey('items.name'))
    quantity = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    item = relationship('Items', back_populates='materials')
    production = relationship('Production', back_populates='materials')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Material(id={self.id}, name={self.name}, production_id={self.production_id})"


class Skill(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True)
    production_id = Column(Integer, ForeignKey('production.id'))
    experience = Column(Float, nullable=False)
    level = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    boostable = Column(Boolean, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    production = relationship('Production', back_populates='skills')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Skill(id={self.id}, name={self.name}, level={self.level}, experience={self.experience}, " \
               f"production_id={self.production_id})"
