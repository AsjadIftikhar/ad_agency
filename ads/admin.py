from django.contrib import admin
from .models import Brand, Campaign, Spend


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_budget', 'daily_budget', 'current_monthly_spend', 'current_daily_spend')

    def current_monthly_spend(self, obj):
        return f"{obj.get_current_monthly_spend():.2f}"

    def current_daily_spend(self, obj):
        return f"{obj.get_current_daily_spend():.2f}"


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'is_active', 'start_hour', 'end_hour')
    list_filter = ('is_active', 'brand')
    actions = ['activate_campaigns', 'deactivate_campaigns']

    def activate_campaigns(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_campaigns(self, request, queryset):
        queryset.update(is_active=False)

    activate_campaigns.short_description = "Activate selected campaigns"
    deactivate_campaigns.short_description = "Deactivate selected campaigns"


@admin.register(Spend)
class SpendAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'brand', 'amount', 'date')
    list_filter = ('date', 'brand')
    date_hierarchy = 'date'

    def brand(self, obj):
        return obj.campaign.brand
