from fastapi import APIRouter
from app.wallet.dependencies import (insert_to_db,
                          get_wallets_from_db,
                          get_wallet_by_id,
                          operation_with_wallet,
                          SessionDep)
from app.wallet.schemas import (WalletResponse,
                         WalletCreateRequest,
                         WalletsListResponse,
                         WalletOperationRequest,
                         WalletOperationResponse)



router = APIRouter(prefix='/api/v1', tags=['wallet'])


@router.get('/wallets', response_model=WalletsListResponse, summary='wallets')
def get_wallets_list(session: SessionDep):
    list_wallets = get_wallets_from_db(session)
    return WalletsListResponse(wallets=list_wallets)


@router.post('/wallets')
def create_wallet(session: SessionDep, new_wallet: WalletCreateRequest):
    wallet = insert_to_db(session, new_wallet.balance)
    return {'new_wallet': wallet}


@router.get('/wallets/{wallet_id}', response_model=WalletResponse)
def get_wallet(session: SessionDep, wallet_id) -> WalletResponse:
    wallet = get_wallet_by_id(session, wallet_id)
    return WalletResponse(wallet_id=wallet.id, balance=wallet.balance)


@router.post('/wallets/{wallet_id}/operation', response_model=WalletOperationResponse)
def wallet_operation(session: SessionDep, wallet_id, operation_data: WalletOperationRequest):
    updated_wallet = operation_with_wallet(
        session, wallet_id, operation_data.operation_type, operation_data.amount
    )
    return WalletOperationResponse(
        wallet_id=updated_wallet.id,
        balance=updated_wallet.balance,
        message=updated_wallet.message,
    )