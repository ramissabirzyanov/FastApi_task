import pytest
import os
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.main import app
from app.database import get_session
from fastapi.testclient import TestClient


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_TEST_NAME')


TEST_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
)
ENGINE = create_engine(TEST_DATABASE_URL)
SessionLocalTest = sessionmaker(bind=ENGINE, expire_on_commit=False, autoflush=False)

Base.metadata.create_all(bind=ENGINE)


@pytest.fixture()
def test_db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = ENGINE.connect()
    transaction = connection.begin()
    test_session = SessionLocalTest(bind=connection)
    yield test_session
    test_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(test_db_session):

    def override_get_session():
        try:
            yield test_db_session
        finally:
            test_db_session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def create_wallet():

    return {
        "balance": str(Decimal(10000)),
    }


@pytest.fixture
def deposit_operation():

    return {
        "operation_type": "deposit",
        "amount": str(Decimal(5000)),
    }


@pytest.fixture
def withdraw_operation():

    return {
        "operation_type": "withdraw",
        "amount": str(Decimal(12000)),
    }
