"""
Deposits app configuration.
"""

from django.apps import AppConfig


class DepositsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.deposits'
    verbose_name = 'Deposits Management'
    
    def ready(self):
        """Import signals when app is ready."""
        import apps.deposits.signals
