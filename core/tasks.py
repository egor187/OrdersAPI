from core.celery_app import app
from .models import Client
from django.utils import timezone
from requests import RequestException
from connectors import BaseAPIConnector


@app.task(
    bind=True,
    ignore_result=True,
    autoretry_for=(RequestException,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=10,
)
def run_campaign(campaign):
    if campaign.check_in_time():
        clients = Client.objects.filter(**campaign.settings)
        while timezone.now() < campaign.finished_at:
            for client in clients:
                client_messages = client.messages
                for message in client_messages:
                    connector = BaseAPIConnector(client=client, message=message)
                    connector.send_request()
