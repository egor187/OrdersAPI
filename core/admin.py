from django.contrib import admin

from .models import Client, Message, Campaign, Statistic


class CampaignAdmin(admin.ModelAdmin):
    readonly_fields = ('completed_at',)


admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Statistic)
admin.site.register(Campaign, CampaignAdmin)
