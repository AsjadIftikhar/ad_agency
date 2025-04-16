from django.db import models
from django.utils import timezone
import calendar

class Brand(models.Model):
    name = models.CharField(max_length=100)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
    def get_current_daily_spend(self):
        today = timezone.now().date()
        return self.spends.filter(date=today).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    def get_current_monthly_spend(self):
        now = timezone.now()
        return self.spends.filter(
            date__year=now.year, 
            date__month=now.month
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    def is_daily_budget_exceeded(self):
        return self.get_current_daily_spend() >= self.daily_budget
    
    def is_monthly_budget_exceeded(self):
        return self.get_current_monthly_spend() >= self.monthly_budget

class Campaign(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='campaigns')
    is_active = models.BooleanField(default=True)
    start_hour = models.IntegerField(null=True, blank=True)
    end_hour = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def should_be_active_now(self):
        if self.start_hour is not None and self.end_hour is not None:
            current_hour = timezone.now().hour
            if not (self.start_hour <= current_hour < self.end_hour):
                return False
        
        if self.brand.is_daily_budget_exceeded() or self.brand.is_monthly_budget_exceeded():
            return False
            
        return True

class Spend(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='spends')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='spends')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.campaign.name} - {self.amount} on {self.date}"