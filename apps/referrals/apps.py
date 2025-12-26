from django.apps import AppConfig


class ReferralsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.referrals'
    
    def ready(self):
        import apps.referrals.signals
