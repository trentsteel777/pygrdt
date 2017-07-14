from django.apps import AppConfig


class AnalysisportalConfig(AppConfig):
    name = 'analysisportal'
    def ready(self):
        from django_celery_beat.models import CrontabSchedule, PeriodicTask
        
        # If Scrape_Nasdaq_Website isn't setup then create it
        try:
            PeriodicTask.objects.get(name='Scrape_Nasdaq_Website')
        except PeriodicTask.DoesNotExist:
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute='*',
                hour='*/1',
                day_of_week='1-5',
                day_of_month='*',
                month_of_year='*',
            )   
    
            PeriodicTask.objects.create(
                crontab=schedule,
                name='Scrape_Nasdaq_Website',
                task='analysisportal.tasks.scrapeNasdaqWebsite',
            )    
