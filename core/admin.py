from django.contrib import admin

from .models import Client, Message, Campaign


class CampaignAdmin(admin.ModelAdmin):
    readonly_fields = ('completed_at',)


admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Campaign, CampaignAdmin)
