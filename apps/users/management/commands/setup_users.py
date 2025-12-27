from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin and test user'

    def handle(self, *args, **options):
        # Create admin
        if not User.objects.filter(email='admin@example.com').exists():
            admin = User.objects.create_user(
                email='admin@example.com',
                username='admin@example.com',
                first_name='Admin',
                last_name='User',
                password='admin123456',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin created: admin@example.com / admin123456'))
        else:
            self.stdout.write(self.style.WARNING('• Admin already exists'))

        # Create test user
        if not User.objects.filter(email='user@example.com').exists():
            user = User.objects.create_user(
                email='user@example.com',
                username='user@example.com',
                first_name='Test',
                last_name='User',
                password='user123456'
            )
            self.stdout.write(self.style.SUCCESS('✓ User created: user@example.com / user123456'))
        else:
            self.stdout.write(self.style.WARNING('• User already exists'))

        self.stdout.write(self.style.SUCCESS('\n✓ Setup complete!'))
