import pytest
import pytest_asyncio
import asyncio
import sys

from sqlalchemy.exc import IntegrityError

from sql.database import async_session
from sql import models, schemas, crud


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def db_session():
    db = async_session()
    yield db


@pytest.mark.asyncio
class TestDB:
    async def test_create_item(self, db_session):
        item = schemas.ItemCreate(id=1, name="Test Cannonball", market=1000, limit=5000, members=True, high_alch=10, low_alch=5)
        db = db_session

        async with db as session:
            result = await crud.create_item(session, item)

        assert isinstance(result, models.Items), "result is not an Item type"
        assert result.id == 1, "Correct ID was not returned in query"

    @pytest.mark.xfail(raises=IntegrityError)
    async def test_create_item_fail(self, db_session):
        item = schemas.ItemCreate(id=1, name="Cannonball", market=1000, limit=5000, members=True, high_alch=10,
                                  low_alch=5)
        db = db_session

        async with db as session:
            await crud.create_item(session, item)

    async def test_create_category(self, db_session):
        cat = schemas.CategoryCreate(name='PyTest', item_id=1)
        db = db_session
        async with db as session:
            result = await crud.create_category(session, cat)

        assert isinstance(result, models.Category), "result is not a Category type"
        assert result.name == 'PyTest', 'Incorrect category name'

    async def test_get_item(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_item(session, item_id=1)

        assert isinstance(result, models.Items), "result is not an Item type"
        assert result.id == 1, "Correct ID was not returned in query"

    async def test_update_item(self, db_session):
        item = schemas.ItemCreate(id=1, name="Cannonball", market=1, limit=5000, members=True, high_alch=10, low_alch=5)
        db = db_session

        async with db as session:
            await crud.update_item(session, item)
            result = await crud.get_item(session, item_id=1)

        assert isinstance(result, models.Items), "result is not an Item type"
        assert result.market == 1, "Correct market was not returned in query"

    async def test_get_category(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_category(session, cat_id=1)

        assert isinstance(result, models.Category), "result is not a Category type"
        assert result.name == "PyTest", "Correct name was not returned in query"

    async def test_get_category_by_item(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_category_by_item(session, item_id=1)

        assert isinstance(result, list), "result is not a list type"

        assert isinstance(result[0], models.Category), "result does not contain Category type"
        assert result[0].name == 'PyTest', 'Incorrect category name'

    async def test_create_average(self, db_session):
        db_add = schemas.AverageCreate(item_id=1, low_price=1, high_price=10, low_volume=10, high_volume=25)
        db = db_session
        async with db as session:
            result = await crud.create_average(session, db_add)

        assert isinstance(result, models.Average), "result is not an Average type"

    async def test_create_daily(self, db_session):
        db_add = schemas.DailyCreate(item_id=1, price=25, volume=1000)
        db = db_session
        async with db as session:
            result = await crud.create_daily(session, db_add)

        assert isinstance(result, models.Daily), "result is not a Daily type"

    @pytest.mark.xfail(raises=IntegrityError)
    async def test_create_daily_duplicate(self, db_session):
        # Cannot create a duplicate date stamp (unique enforced in table)
        db_add = schemas.DailyCreate(item_id=1, price=50, volume=1500)
        db = db_session
        async with db as session:
            result = await crud.create_daily(session, db_add)

    async def test_create_latest(self, db_session):
        db_add = schemas.LatestCreate(item_id=1, low_price=1, high_price=10)
        db = db_session
        async with db as session:
            result = await crud.create_latest(session, db_add)

        assert isinstance(result, models.Latest), "result is not a Latest type"

    async def test_get_average(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_average(session, average_id=1)

        assert isinstance(result, models.Average), "result is not an Average type"
        assert result.item_id == 1, 'Result has the incorrect item ID'
        assert result.low_price == 1, 'Result does not have correct low price'

    async def test_get_average_by_item(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_average_by_item(session, item_id=1)

        assert isinstance(result, list), "result is not a list type"
        assert isinstance(result[0], models.Average), "result[0] is not a Average type"
        assert result[0].item_id == 1, 'Result has the incorrect item ID'
        assert result[0].low_price == 1, 'Result does not have correct low price'

    async def test_get_daily(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_daily(session, daily_id=1)

        assert isinstance(result, models.Daily), "result is not a Daily type"
        assert result.item_id == 1, 'Result has the incorrect item ID'
        assert result.price == 25, 'Result does not have correct low price'

    async def test_get_daily_by_item(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_daily_by_item(session, item_id=1)

        assert isinstance(result, list), "result is not a list type"
        assert isinstance(result[0], models.Daily), "result[0] is not a Daily type"
        assert result[0].item_id == 1, 'Result has the incorrect item ID'
        assert result[0].price == 25, 'Result does not have correct low price'

    async def test_get_latest(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_latest(session, latest_id=1)

        assert isinstance(result, models.Latest), "result is not a Latest type"
        assert result.item_id == 1, 'Result has the incorrect item ID'
        assert result.low_price == 1, 'Result does not have correct price'

    async def test_get_latest_by_item(self, db_session):
        db = db_session
        async with db as session:
            result = await crud.get_latest_by_item(session, item_id=1)

        assert isinstance(result, list), "result is not a list type"
        assert isinstance(result[0], models.Latest), "result[0] is not a Latest type"
        assert result[0].item_id == 1, 'Result has the incorrect item ID'
        assert result[0].low_price == 1, 'Result does not have correct price'
