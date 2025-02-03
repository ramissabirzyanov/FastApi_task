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


@pytest.fixture
def test_db_session():
    DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
    )
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    LocalSessionTest = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    test_session = LocalSessionTest()
    yield test_session
    test_session.close()
    Base.metadata.drop_all(engine)

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
