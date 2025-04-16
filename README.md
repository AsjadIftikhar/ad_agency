# Ad Agency Budget Management System

A Django application that manages advertising campaigns for brands with budget constraints and dayparting rules.

## Features
- Brand budget tracking (daily/monthly)
- Automatic campaign activation/deactivation
- Dayparting functionality
- Budget monitoring and spend tracking

## Setup & Running

### Prerequisites
- Python 3.8+, Django, Redis, Celery

### Quick Start
```bash
# Install dependencies
pip install django celery redis django-celery-beat

# Start Redis
brew install redis
brew services start redis

# Setup database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run the application
python manage.py runserver
celery -A ad_agency worker -l info
celery -A ad_agency beat -l info

# Test with simulated spend
python manage.py simulate_spend
```

### Assumptions
- Ignored using environment variables as its a dummy project
- Budgets reset at midnight (daily) and month start
- Campaigns active by default when created
- Spend recorded at campaign level

### Data Models
- Brand : Stores client info with daily/monthly budgets
- Campaign : Links to Brand with activation status and dayparting settings
- Spend : Records spending events with amount and date

### Program Flow
1. Celery tasks monitor campaign status hourly
2. Campaigns auto-deactivate when:
   - Daily/monthly budget exceeded
   - Outside dayparting hours
3. Campaigns auto-reactivate at start of day/month if budget allows