"""
Withdrawals app configuration.
"""

from django.apps import AppConfig


class WithdrawalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.withdrawals'
    verbose_name = 'Withdrawals Management'
    
    def ready(self):
        """Import signals when app is ready."""
        import apps.withdrawals.signals
