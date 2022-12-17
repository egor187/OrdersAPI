import pytest
from core import models
from django.utils import timezone

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_campaign_create(mocked_celery_api):
    assert models.Campaign.objects.count() == 1
    mocked_celery_api.assert_called_once()
    models.Campaign.objects.create(
        started_at=timezone.now(),
        finished_at=timezone.now() + timezone.timedelta(days=1),
        message='Test',
        settings={'cell_phone': '+79992222222'}
    )
    assert mocked_celery_api.call_count == 2
    assert models.Campaign.objects.count() == 2


