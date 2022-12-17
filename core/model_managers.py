from django.db import models
from django.db.transaction import atomic
from celery import current_app


class CampaignManager(models.Manager):
    @atomic()
    def create(self, **kwargs):
        obj = super().create(**kwargs)
        current_app.send_task(
            'core.tasks.run_campaign',
            kwargs={'campaign_settings': obj.settings, 'campaign_finished_at': obj.finished_at},
            countdown=obj.get_task_countdown()
        )
        return obj
