"""
Management command to generate referral codes for existing users.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate referral codes for users who do not have one'

    def handle(self, *args, **options):
        users_updated = 0
        users_without_code = User.objects.filter(referral_code__isnull=True) | User.objects.filter(referral_code='')
        
        for user in users_without_code:
            user.referral_code = str(uuid.uuid4())[:8].upper()
            user.save()
            users_updated += 1
            self.stdout.write(f'Generated referral code for {user.username}: {user.referral_code}')
        
        if users_updated > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully generated referral codes for {users_updated} user(s)'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('All users already have referral codes')
            )
