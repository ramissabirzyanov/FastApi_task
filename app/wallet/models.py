from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from decimal import Decimal
import uuid
import datetime


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=3), default=0)


class WalletOperation(Base):
    __tablename__ = "wallet_operation"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Wallet.id))
    operation_type: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=3), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                    server_default=func.now(),
                                                    onupdate=func.now(),
                                                    default=datetime.datetime.now)
