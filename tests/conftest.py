import contextlib
from unittest import mock

import pytest

from cbpro import authenticated_client
from cbpro import public_client


@contextlib.contextmanager
def patch_messaging(client):
    with mock.patch.multiple(
            client,
            _send_message=mock.DEFAULT,
            _send_paginated_message=mock.DEFAULT,
            autospec=True,
    ):
        yield client


@pytest.fixture
def pub_client():
    """A dummy client for testing."""
    client = public_client.PublicClient()
    with patch_messaging(client):
        yield client


@pytest.fixture
def auth_client():
    """Mocks out sending messages."""
    client = authenticated_client.AuthenticatedClient('test', 'test', 'test')
    with patch_messaging(client):
        yield client
