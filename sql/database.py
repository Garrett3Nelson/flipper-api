import databases
import sqlalchemy

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database('postgresql+asyncpg://localhost/example', ssl=True, min_size=5, max_size=20)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL
)

