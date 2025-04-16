from celery import shared_task
from django.utils import timezone
from .models import Brand, Campaign, Spend


@shared_task
def check_campaign_status():
    campaigns = Campaign.objects.all()

    for campaign in campaigns:
        should_be_active = campaign.should_be_active_now()

        if campaign.is_active != should_be_active:
            campaign.is_active = should_be_active
            campaign.save()


@shared_task
def reset_daily_campaigns():
    brands = Brand.objects.all()

    for brand in brands:
        if brand.is_monthly_budget_exceeded():
            continue

        for campaign in brand.campaigns.all():
            if not campaign.is_active:
                campaign.is_active = True
                campaign.save()


@shared_task
def reset_monthly_campaigns():
    campaigns = Campaign.objects.filter(is_active=False)

    for campaign in campaigns:
        campaign.is_active = True
        campaign.save()


@shared_task
def record_spend(campaign_id, amount):
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        Spend.objects.create(
            brand=campaign.brand,
            campaign=campaign,
            amount=amount,
            date=timezone.now().date()
        )

        if campaign.brand.is_daily_budget_exceeded() or campaign.brand.is_monthly_budget_exceeded():
            if campaign.is_active:
                campaign.is_active = False
                campaign.save()

    except Campaign.DoesNotExist:
        pass
