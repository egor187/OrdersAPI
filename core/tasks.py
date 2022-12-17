from core.celery_app import app
from .models import Client
from django.utils import timezone
from requests import RequestException
from .connectors import BaseAPIConnector


@app.task(
    ignore_result=True,
    autoretry_for=(RequestException,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=10,
)
def run_campaign(campaign_settings, campaign_finished_at):
    clients = Client.objects.filter(**campaign_settings).prefetch_related('messages')
    while timezone.now() < campaign_finished_at and clients:
        for client in clients:
            client_messages = client.messages.all()
            for message in client_messages:
                connector = BaseAPIConnector(client=client, message=message)
                connector.send_request()
            clients = clients.exclude(pk=client.pk)
