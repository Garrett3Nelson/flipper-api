from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean
from .database import metadata

master_items = Table(
    "master_items",
    metadata,
    Column('id', Integer, primary_key=True, auto_increment=False),
    Column('name', String(100)),
    Column('market', Integer),
    Column('limit', Integer),
    Column('members', Boolean),
    Column('highalch', Integer),
    Column('lowalch', Integer),

    # Categories Table reference
    # Price History Table reference
    # Volume History Table
    # Production History
)
