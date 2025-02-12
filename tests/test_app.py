def test_get_wallets_list(test_client):
    response = test_client.get('/api/v1/wallets')
    assert response.status_code == 200
    assert 'wallets' in response.json()
    assert response.json()['wallets'] == []


def test_create_wallet(test_client, create_wallet):
    response = test_client.post('/api/v1/wallets', json=create_wallet)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["new_wallet"]["balance"] == 10000
    get_response = test_client.get('/api/v1/wallets')
    assert len(get_response.json()['wallets']) == 1


def test_get_wallet_by_wallet_id(test_client, create_wallet):
    new_wallet = test_client.post('/api/v1/wallets', json=create_wallet)
    new_wallet_id = new_wallet.json()["new_wallet"]["id"]
    get_new_wallet = test_client.get(f'/api/v1/wallets/{new_wallet_id}')
    assert get_new_wallet.status_code == 200
    assert 'balance' and 'wallet_id' in get_new_wallet.json()


def test_wallet_operation(test_client, create_wallet, deposit_operation, withdraw_operation):
    wallet = test_client.post('/api/v1/wallets', json=create_wallet)
    wallet_id = wallet.json()["new_wallet"]["id"]
    response_deposit = test_client.post(
        f'/api/v1/wallets/{wallet_id}/operation', json=deposit_operation
    )
    assert response_deposit.status_code == 200
    wallet_after_operation = test_client.get(f'/api/v1/wallets/{wallet_id}')
    assert wallet_after_operation.json()['balance'] == "15000.000"
    response_withdraw = test_client.post(
        f'/api/v1/wallets/{wallet_id}/operation', json=withdraw_operation
    )
    assert response_withdraw.status_code == 200
    wallet_after_operation = test_client.get(f'/api/v1/wallets/{wallet_id}')
    assert wallet_after_operation.json()['balance'] == "3000.000"
