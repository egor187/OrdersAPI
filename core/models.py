from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField
from django.utils import timezone
from .validators import validate_campaign_settings
from celery import current_app


class Client(models.Model):
    cell_phone = PhoneNumberField(region='RU')
    cell_phone_op_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=32, null=True, blank=True)
    tz = TimeZoneField(use_pytz=True)


class Campaign(models.Model):
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    message = models.TextField()
    settings = models.JSONField(default=dict, validators=[validate_campaign_settings], null=True, blank=True)

    @property
    def check_in_time(self):
        return self.finished_at <= timezone.now() <= self.started_at

    def get_task_countdown(self):
        return 0 if self.check_in_time else (self.finished_at - timezone.now()).seconds

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        current_app.send_task('core.tasks.run_campaign', countdown=self.get_task_countdown())


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32, choices=(('CREATED', 'Created'), ('PENDING', 'Pending'), ('FINISHED', 'Finished'))
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')


class Statistic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    api_response = models.JSONField(default=dict)
