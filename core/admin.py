from django.contrib import admin

from .models import Client, Message, Campaign

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Campaign)
