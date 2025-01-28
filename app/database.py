from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker, Session
from fastapi import HTTPException, status, Depends
from app.models import Wallet, WalletOperation
from typing import Annotated
import os
import uuid


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)


ENGINE = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=ENGINE, expire_on_commit=False, autoflush=False)


def get_session():
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_wallets_from_db(session: SessionDep):
    query = select(Wallet)
    wallets = session.execute(query)
    return [
        {'wallet_id': wallet.id, 'balance': wallet.balance} for wallet in wallets.scalars().all()
    ]


def insert_to_db(session: SessionDep, balance, wallet_id=uuid.uuid4()):
    new_wallet = Wallet(
        id=wallet_id,
        balance=balance
    )
    session.add(new_wallet)
    session.commit()
    return new_wallet


def get_wallet_by_id(session: SessionDep, wallet_id):
    query = select(Wallet).where(Wallet.id == wallet_id)
    wallet = session.execute(query).scalar()
    return wallet


def operation_with_wallet(session: SessionDep, wallet_id, operation_type, amount):
    get_wallet_query = select(Wallet).where(Wallet.id == wallet_id)
    wallet = session.execute(get_wallet_query).scalar()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet with id={wallet_id} does not exitst."
        )
    if operation_type.upper() == "DEPOSIT":
        new_balance = wallet.balance + amount
    elif operation_type.upper() == "WITHDRAW":
        if wallet.balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have so much!"
            )
        new_balance = wallet.balance - amount
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Wrong operation type. Use DEPOSIT or WITHDRAW!"
        )

    update_wallet_balance_query = update(Wallet).\
        where(Wallet.id == wallet_id).\
        values(balance=new_balance)
    session.execute(update_wallet_balance_query)
    new_wallet_operation = WalletOperation(
        wallet_id=wallet_id,
        operation_type=operation_type.upper(),
        amount=amount
    )
    session.add(new_wallet_operation)
    session.commit()
    session.close()
    updated_result = get_wallet_by_id(session, wallet_id)
    updated_result.message = 'Success'
    return updated_result
