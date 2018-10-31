import pytest


class TestAuthenticatedClientSyntax:

    def test_place_order_input_1(self, auth_client):
        with pytest.raises(ValueError):
            auth_client.place_order(
                'BTC-USD',
                'buy',
                'market',
                overdraft_enabled='true',
                funding_amount=10,
            )

    def test_place_order_input_2(self, auth_client):
        with pytest.raises(ValueError):
            auth_client.place_order(
                'BTC-USD',
                'buy',
                'limit',
                cancel_after='123',
                time_in_force='ABC',
            )

    def test_place_order_input_3(self, auth_client):
        with pytest.raises(ValueError):
            auth_client.place_order(
                'BTC-USD',
                'buy',
                'limit',
                post_only='true',
                time_in_force='FOK',
            )

    def test_place_order_input_4(self, auth_client):
        with pytest.raises(ValueError):
            auth_client.place_order(
                'BTC-USD',
                'buy',
                'market',
                size=None,
                funds=None,
            )

    def test_place_order_input_5(self, auth_client):
        with pytest.raises(ValueError):
            auth_client.place_order(
                'BTC-USD',
                'buy',
                'market',
                size=1,
                funds=1,
            )


class TestAccountCalls():
    def test_get_account(self, auth_client):
        account = {
            'id': 'e316cb9a-0808-4fd7-8914-97829c1925de',
            'currency': 'USD',
            'balance': '80.2301373066930000',
            'available': '79.2266348066930000',
            'hold': '1.0035025000000000',
            'profile_id': '75da88c5-05bf-4f54-bc85-5c775bd68254',
        }
        auth_client._send_message.return_value = account
        returned_account = auth_client.get_account(
            'e316cb9a-0808-4fd7-8914-97829c1925de',
        )
        assert returned_account == account

    def test_get_accounts(self, auth_client):
        accounts = [
            {
                'id': '71452118-efc7-4cc4-8780-a5e22d4baa53',
                'currency': 'BTC',
                'balance': '0.0000000000000000',
                'available': '0.0000000000000000',
                'hold': '0.0000000000000000',
                'profile_id': '75da88c5-05bf-4f54-bc85-5c775bd68254',
            },
            {
                'id': 'e316cb9a-0808-4fd7-8914-97829c1925de',
                'currency': 'USD',
                'balance': '80.2301373066930000',
                'available': '79.2266348066930000',
                'hold': '1.0035025000000000',
                'profile_id': '75da88c5-05bf-4f54-bc85-5c775bd68254',
            }
        ]
        auth_client._send_message.return_value = accounts
        returned_accounts = auth_client.get_accounts()
        assert returned_accounts == accounts

    def test_get_account_history(self, auth_client):
        history = [
            {
                "id": "100",
                "created_at": "2014-11-07T08:19:27.028459Z",
                "amount": "0.001",
                "balance": "239.669",
                "type": "fee",
                "details": {
                    "order_id": "d50ec984-77a8-460a-b958-66f114b0de9b",
                    "trade_id": "74",
                    "product_id": "BTC-USD"
                }
            }
        ]
        auth_client._send_paginated_message.return_value = history
        returned_history = auth_client.get_account_history(
            'acct-id',
            additional_kwarg=True,
        )
        assert returned_history == history

    def test_get_account_holds(self, auth_client):
        holds = [
            {
                "id": "82dcd140-c3c7-4507-8de4-2c529cd1a28f",
                "account_id": "e0b3f39a-183d-453e-b754-0c13e5bab0b3",
                "created_at": "2014-11-06T10:34:47.123456Z",
                "updated_at": "2014-11-06T10:40:47.123456Z",
                "amount": "4.23",
                "type": "order",
                "ref": "0a205de4-dd35-4370-a285-fe8fc375a273",
            }
        ]
        auth_client._send_paginated_message.return_value = holds
        returned_holds = auth_client.get_account_holds(
            'acct-id',
            additional_kwarg=True,
        )
        assert returned_holds == holds
