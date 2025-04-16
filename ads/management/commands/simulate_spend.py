from django.core.management.base import BaseCommand
from ads.models import Campaign
from ads.tasks import record_spend
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Simulates ad spend for active campaigns'

    def handle(self, *args, **options):
        active_campaigns = Campaign.objects.filter(is_active=True)
        
        for campaign in active_campaigns:
            amount = Decimal(random.randint(100, 10000)) / Decimal(100)
            
            self.stdout.write(f"Recording ${amount} spend for {campaign.name}")
            
            record_spend.delay(campaign.id, amount)
        
        self.stdout.write(self.style.SUCCESS('Successfully simulated ad spend'))