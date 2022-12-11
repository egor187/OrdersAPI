from django.db import models
from phonenumber_field.formfields import PhoneNumberField
from timezone_field import TimeZoneField
from django.utils import timezone


class Client(models.Model):
    cell_phone = PhoneNumberField(region='RU')
    cell_phone_op_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=32, null=True, blank=True)
    tz = TimeZoneField(use_pytz=True)


class Campaign(models.Model):
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
    message = models.TextField(null=True)
    settings = models.JSONField(default=dict)

    def check_status(self):
        return self.finished_at <= timezone.now()


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32, choices=(('CREATED', 'Created'), ('PENDING', 'Pending'), ('FINISHED', 'Finished'))
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
