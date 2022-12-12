from django.core.exceptions import ValidationError
from django.apps import apps


def validate_campaign_settings(value):
    client_model = apps.get_model('core.Client')
    client_fields = [field.name for field in client_model._meta.fields]
    client_fields.remove('id')
    if not all(
            [key in client_fields for key in value.keys()]
    ):
        raise ValidationError(
            f'Incorrect campaign settings. Settings must only include CLIENT attributes: {client_fields}'
        )
