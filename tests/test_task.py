from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from django.utils.timezone import make_aware
from freezegun import freeze_time
from core.tasks import run_campaign

pytestmark = pytest.mark.django_db

NOW = make_aware(datetime(2022, 12, 12, 0, 0, 0))
TEN_SECONDS_LATER = NOW + timedelta(seconds=10)


@freeze_time(NOW)
@pytest.mark.parametrize(
    'campaign_settings, campaign_finished_at, expected_calls', (
        (
            {'cell_phone': '+79999999999'},
            TEN_SECONDS_LATER,
            1
        ),
        (
            {'cell_phone': '+79991111111'},
            TEN_SECONDS_LATER,
            2
        ),
        (
            {'tag': 'tagged'},
            TEN_SECONDS_LATER,
            10
        ),
        (
            {'tag': 'test tag'},
            TEN_SECONDS_LATER,
            1
        ),
    )
)
def test_run_campaign(connector, client, message, five_tagged_clients, campaign_settings, campaign_finished_at, expected_calls):
    with patch('core.connectors.requests.post', return_value={'code': 0, 'msg': 'test'}) as mock:
        run_campaign(campaign_settings, campaign_finished_at)
        assert mock.call_count == expected_calls
