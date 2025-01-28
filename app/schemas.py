from pydantic import BaseModel, ConfigDict, Field, UUID4
from decimal import Decimal
from typing import List


class WalletCreateRequest(BaseModel):
    balance: Decimal = Field(default=0)

    model_config = ConfigDict(extra='forbid')


class WalletResponse(BaseModel):
    wallet_id: UUID4
    balance: Decimal


class WalletsListResponse(BaseModel):
    wallets: List[WalletResponse]


class WalletOperationRequest(BaseModel):
    operation_type: str = Field(default='DEPOSIT')
    amount: Decimal

    model_config = ConfigDict(extra='forbid')


class WalletOperationResponse(BaseModel):
    wallet_id: UUID4
    balance: Decimal
    message: str
