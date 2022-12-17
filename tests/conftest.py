from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time
from django.utils.timezone import now, make_aware, timedelta
from datetime import datetime
from django.utils.module_loading import import_string

from core.models import Campaign, Client, Message
from core.connectors import BaseAPIConnector


def func_proxy():
    """
    Allows to replace celery api calls with real function calls.
    """

    def inner(*args, **kwargs):
        func = import_string(args[0])
        args = kwargs.get('args', ()) or () if len(args) < 2 else args[1] or ()
        kwargs = kwargs.get('kwargs', {}) or {}
        result = func(*args, **kwargs)

        class Proxy:
            id = '123'
            def get(self, *args, **kwargs):
                return result

        return Proxy()

    return inner


@pytest.fixture
def mocked_celery_api():
    with patch('celery.current_app.send_task', MagicMock(side_effect=func_proxy())) as mock:
        yield mock


@pytest.fixture(autouse=True)
def campaign(mocked_celery_api):
    campaign = Campaign.objects.create(
        started_at=now(),
        finished_at=now() + timedelta(days=1),
        message='Hello world',
        settings={'cell_phone': '+79991111111'}
    )
    yield campaign


@pytest.fixture
def client():
    cl = Client.objects.create(
        cell_phone='+79999999999',
        cell_phone_op_code='999',
        tag='test tag',
    )
    yield cl


@pytest.fixture
def five_tagged_clients(campaign):
    tag = 'tagged'
    for _ in range(5):
        client = Client.objects.create(cell_phone=f'+7999111111{_}', cell_phone_op_code='111', tag=tag)
        [Message.objects.create(campaign=campaign, status='CREATED', client=client) for _ in range(2)]


@freeze_time(make_aware(datetime(2022, 12, 12, 0, 0, 0)))
@pytest.fixture
def message(campaign, client):
    msg = Message.objects.create(
        campaign=campaign,
        status='CREATED',
        client=client
    )
    return msg


@pytest.fixture
def connector(client, message):
    return BaseAPIConnector(client, message)


@pytest.fixture
def mocked_connector(request):
    marker = request.node.get_closest_marker('connector_mocked_results')
    return_value = marker.args[0] if marker else {'send_request2': {'code': 0, 'msg': 'test response'}}
    with patch(
            'core.connectors.BaseAPIConnector', return_value=MagicMock(
                **{key: MagicMock(return_value=value) for key, value in return_value.items()}
            )
    ) as new_connector:
        yield new_connector
