from django.contrib import admin
from .models import ExchangeProposal


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender_display', 'ad_receiver_display', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('comment', 'ad_sender__title', 'ad_receiver__title')

    def ad_sender_display(self, obj):
        return f"{obj.ad_sender.title} (by {obj.ad_sender.user.username})"

    ad_sender_display.short_description = 'Предлагаемый товар'

    def ad_receiver_display(self, obj):
        return f"{obj.ad_receiver.title} (by {obj.ad_receiver.user.username})"

    ad_receiver_display.short_description = 'Запрашиваемый товар'