from unittest import mock

import pytest

import cbpro


class TestClientMessaging:

    def test_send_message(self):
        client = cbpro.PublicClient()
        with mock.patch.object(client.session, 'request'):
            client._send_message(
                'post',
                '/endpoint',
                params={},
                data={},
            )
            client.session.request.assert_called_with(
                'post',
                client.url + '/endpoint',
                params={},
                data={},
                auth=client.auth,
                timeout=client.timeout,
            )

    def test_paginated_messaging(self):
        client = cbpro.PublicClient()
        with mock.patch.object(client.session, 'get'):
            result = mock.MagicMock()
            result.json.return_value = [1]
            result.headers.__getitem__.side_effect = ['a', None]
            client.session.get.return_value = result

            paginated_results = client._send_paginated_message(
                '/paginated',
                params={},
            )

            expected_params = [{}, {'after': 'a'}, {'after': None}]

            for i, result in enumerate(paginated_results):
                client.session.get.assert_called_with(
                    client.url + '/paginated',
                    params=expected_params[i],
                    auth=client.auth,
                    timeout=client.timeout,
                )


class TestPublicClientInterface(object):

    def test_get_products(self, pub_client):
        products = [
            {
                "id": "BTC-USDC",
                "base_currency": "BTC",
                "quote_currency": "USDC",
                "base_min_size": "0.00100000",
                "base_max_size": "70.00000000",
                "quote_increment": "0.01000000",
                "display_name": "BTC/USDC",
                "status": "online",
                "margin_enabled": False,
                "status_message": "",
                "min_market_funds": "10",
                "max_market_funds": "1000000",
                "post_only": False,
                "limit_only": False,
                "cancel_only": False,
            },
            {
                "id": "ETH-USDC",
                "base_currency": "ETH",
                "quote_currency": "USDC",
                "base_min_size": "0.01000000",
                "base_max_size": "700.00000000",
                "quote_increment": "0.01000000",
                "display_name": "ETH/USDC",
                "status": "online",
                "margin_enabled": False,
                "status_message": "",
                "min_market_funds": "10",
                "max_market_funds": "1000000",
                "post_only": False,
                "limit_only": False,
                "cancel_only": False,
            },
        ]
        pub_client._send_message.return_value = products
        returned_products = pub_client.get_products()
        assert returned_products == products
        pub_client._send_message.assert_called_with(
            'get',
            '/products',
        )

    def test_get_product_order_book(self, pub_client):
        orders = {
            "sequence": 5661101509,
            "bids": [
                [
                    "194.77",
                    "14.52299794",
                    2,
                ],
            ],
            "asks": [
                [
                    "194.78",
                    "64.21370747",
                    4,
                ],
            ],
        }
        pub_client._send_message.return_value = orders
        assert pub_client.get_product_order_book('product', level=1) == orders
        pub_client._send_message.assert_called_with(
            'get',
            '/products/product/book',
            params={'level': 1},
        )

    def test_get_product_ticker(self, pub_client):
        ticker_info = {
            "trade_id": 4729088,
            "price": "333.99",
            "size": "0.193",
            "bid": "333.98",
            "ask": "333.99",
            "volume": "5957.11914015",
            "time": "2015-11-14T20:46:03.511254Z",
        }
        pub_client._send_message.return_value = ticker_info
        assert pub_client.get_product_ticker('product') == ticker_info
        pub_client._send_message.assert_called_with(
            'get',
            '/products/product/ticker',
        )

    def test_get_product_trades(self, pub_client):
        trades = [
            {
                "time": "2014-11-07T22:19:28.578544Z",
                "trade_id": 74,
                "price": "10.00000000",
                "size": "0.01000000",
                "side": "buy",
            }, {
                "time": "2014-11-07T01:08:43.642366Z",
                "trade_id": 73,
                "price": "100.00000000",
                "size": "0.01000000",
                "side": "sell",
            },
        ]
        pub_client._send_paginated_message.return_value = trades

        product = 'ETH-USD'
        assert pub_client.get_product_trades(
            product,
        ) == trades
        pub_client._send_paginated_message.assert_called_with(
            '/products/{}/trades'.format(product),
        )

    def test_get_product_historic_rates(self, pub_client):
        rates = [
            [
                1540968120,
                194.45,
                194.49,
                194.45,
                194.49,
                2.54,
            ],
            [
                1540968060,
                194.39,
                194.45,
                194.39,
                194.45,
                2.57,
            ],
        ]
        pub_client._send_message.return_value = rates
        product = 'ETH-USD'
        start = '2018-10-10'
        end = '2018-10-11'
        granularity = 60

        assert pub_client.get_product_historic_rates(
            product,
            start=start,
            end=end,
            granularity=granularity,
        ) == rates
        pub_client._send_message.assert_called_with(
            'get',
            '/products/{}/candles'.format(product),
            params={
                'start': start,
                'end': end,
                'granularity': granularity,
            },
        )

    def test_get_product_historic_rates_bad_granularity(self, pub_client):
        with pytest.raises(ValueError):
            pub_client.get_product_historic_rates(
                'product',
                granularity=420,
            )

    def test_get_currencies(self, pub_client):
        currencies = [
            {
                "id": "BTC",
                "name": "Bitcoin",
                "min_size": "0.00000001",
                "status": "online",
                "message": None,
            },
            {
                "id": "EUR",
                "name": "Euro",
                "min_size": "0.01000000",
                "status": "online",
                "message": None,
            },
        ]
        pub_client._send_message.return_value = currencies
        assert pub_client.get_currencies() == currencies
        pub_client._send_message.assert_called_with(
            'get',
            '/currencies',
        )

    def test_get_time(self, pub_client):
        time = {
            "iso": "2018-10-31T06:48:34.184Z",
            "epoch": 1540968514.184,
        }
        pub_client._send_message.return_value = time
        assert pub_client.get_time() == time
        pub_client._send_message.assert_called_with(
            'get',
            '/time',
        )
