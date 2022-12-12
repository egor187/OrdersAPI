# Generated by Django 4.1.4 on 2022-12-12 08:35

import core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField()),
                ('finished_at', models.DateTimeField()),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('message', models.TextField()),
                ('settings', models.JSONField(default=dict, validators=[core.validators.validate_campaign_settings])),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU')),
                ('cell_phone_op_code', models.CharField(max_length=3)),
                ('tag', models.CharField(blank=True, max_length=32, null=True)),
                ('tz', timezone_field.fields.TimeZoneField(use_pytz=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('PENDING', 'Pending'), ('FINISHED', 'Finished')], max_length=32)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.campaign')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.client')),
            ],
        ),
    ]
