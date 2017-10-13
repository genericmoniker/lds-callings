import pytest

from application.database import Database


@pytest.fixture()
def db():
    """A test database that is clean at the start of each test.

    You'll probably also want to patch the db object that the code under test
    is using, such as by making another fixture like so:

    @pytest.fixture(name='db_')
    def web_user_db(db):
        web.user.db = db
        yield db

    """
    database = Database('postgres:///lds-callings-test', echo=False)

    # Drop and recreate all of the tables. If the schema changes enough, this
    # might not work (some leftover tables?). Worst case, just recreate it:
    # $ dropdb lds-callings-test
    # $ createdb lds-callings-test
    database.drop_all()
    database.create_all()
    try:
        yield database
    finally:
        database.cleanup()


