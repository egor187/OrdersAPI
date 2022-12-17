import requests
from django.conf import settings
from settings.env import env
from core.models import Message, Client, Statistic


class BaseAPIConnector:
    default_headers = {'Content-Type': 'application/json', 'Authorization': ''}

    def __init__(self, client: Client, message: Message, url=settings.EXTERNAL_SERVICE_URL, headers=None):
        self.url = f'{url}/{message.id}'
        self.message = message
        self.client = client
        if headers:
            self.default_headers.update(headers)
        self.default_headers['Authorization'] = f'Bearer {str(env("external_service_token"))}'

    def send_request(self):
        try:
            response = requests.post(
                self.url,
                json={
                    'id': self.message.id,
                    'phone': self.message.client.cell_phone,
                    'text': self.message.campaign.message
                },
                headers=self.default_headers
            )
        except requests.RequestException:
            raise

        return self.save_statistic(response, self.message)

    @staticmethod
    def save_statistic(api_response, message):
        return Statistic.objects.create(message=message, api_response=api_response)
