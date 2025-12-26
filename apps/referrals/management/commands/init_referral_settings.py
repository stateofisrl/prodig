"""
Management command to initialize referral settings.
"""

from django.core.management.base import BaseCommand
from apps.referrals.models import ReferralSettings


class Command(BaseCommand):
    help = 'Initialize referral settings with default values'

    def handle(self, *args, **options):
        if not ReferralSettings.objects.exists():
            settings = ReferralSettings.objects.create(
                commission_percentage=5.00,
                is_active=True,
                minimum_deposit_for_commission=0.00,
                max_commission_amount=0.00
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created referral settings with {settings.commission_percentage}% commission rate'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Referral settings already exist')
            )
