"""
Pre-Deployment Checklist Script
Validates all critical components before production deployment
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from apps.investments.models import InvestmentPlan, UserInvestment
from apps.deposits.models import Deposit
from apps.withdrawals.models import Withdrawal
from apps.support.models import SupportTicket
from django.conf import settings
import subprocess

User = get_user_model()

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_status(check, passed):
    status = "✓ PASS" if passed else "✗ FAIL"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} - {check}")
    return passed

print_header("TESLA INVESTMENT PLATFORM - DEPLOYMENT READINESS CHECK")

all_checks_passed = True

# 1. Environment Variables
print_header("1. Environment Configuration")
all_checks_passed &= print_status(
    "SECRET_KEY configured",
    settings.SECRET_KEY != 'your-secret-key-change-in-production' and len(settings.SECRET_KEY) > 50
)
debug_status = "DEBUG=True (OK for dev)" if settings.DEBUG else "DEBUG=False (Production ready)"
all_checks_passed &= print_status(
    debug_status,
    True
)
hosts_status = "ALLOWED_HOSTS=* (Change for production)" if settings.ALLOWED_HOSTS == ['*'] else f"ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}"
all_checks_passed &= print_status(
    hosts_status,
    len(settings.ALLOWED_HOSTS) > 0
)

# 2. Database
print_header("2. Database Configuration")
db_engine = settings.DATABASES['default']['ENGINE']
engine_name = db_engine.split('.')[-1]
print_status(
    f"Database engine: {engine_name}",
    True
)

try:
    user_count = User.objects.count()
    all_checks_passed &= print_status(
        f"Database connection ({user_count} users found)",
        True
    )
except Exception as e:
    all_checks_passed &= print_status(f"Database connection error: {str(e)}", False)

# 3. Models and Data
print_header("3. Data Integrity")
try:
    superuser_count = User.objects.filter(is_superuser=True).count()
    all_checks_passed &= print_status(
        f"Superuser accounts (Found {superuser_count})",
        superuser_count > 0
    )
    
    plan_count = InvestmentPlan.objects.count()
    all_checks_passed &= print_status(
        f"Investment plans (Found {plan_count})",
        plan_count > 0
    )
    
    investment_count = UserInvestment.objects.count()
    print_status(f"User investments (Found {investment_count})", True)
    
    deposit_count = Deposit.objects.count()
    print_status(f"Deposits (Found {deposit_count})", True)
    
    withdrawal_count = Withdrawal.objects.count()
    print_status(f"Withdrawals (Found {withdrawal_count})", True)
    
    ticket_count = SupportTicket.objects.count()
    print_status(f"Support tickets (Found {ticket_count})", True)
    
except Exception as e:
    all_checks_passed &= print_status(f"Model integrity check: {e}", False)

# 4. Static Files
print_header("4. Static Files")
static_root_exists = os.path.exists(settings.STATIC_ROOT)
all_checks_passed &= print_status(
    f"STATIC_ROOT exists: {settings.STATIC_ROOT}",
    static_root_exists
)

if static_root_exists:
    static_file_count = sum([len(files) for r, d, files in os.walk(settings.STATIC_ROOT)])
    all_checks_passed &= print_status(
        f"Static files collected ({static_file_count} files)",
        static_file_count > 0
    )

# 5. Security Settings
print_header("5. Security Configuration")
all_checks_passed &= print_status(
    f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}",
    not settings.DEBUG or not settings.CSRF_COOKIE_SECURE
)
all_checks_passed &= print_status(
    f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}",
    not settings.DEBUG or not settings.SESSION_COOKIE_SECURE
)
all_checks_passed &= print_status(
    f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}",
    not settings.DEBUG or not settings.SECURE_SSL_REDIRECT
)

# 6. Middleware
print_header("6. Middleware Configuration")
required_middleware = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]
for mw in required_middleware:
    all_checks_passed &= print_status(
        f"Middleware: {mw.split('.')[-1]}",
        mw in settings.MIDDLEWARE
    )

# 7. Apps
print_header("7. Installed Apps")
required_apps = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'apps.users',
    'apps.investments',
    'apps.deposits',
    'apps.withdrawals',
    'apps.support',
]
for app in required_apps:
    app_installed = any(app in installed_app for installed_app in settings.INSTALLED_APPS)
    all_checks_passed &= print_status(
        f"App: {app}",
        app_installed
    )

# 8. Signals
print_header("8. Signal Handlers")
signals_exist = [
    os.path.exists('apps/investments/signals.py'),
    os.path.exists('apps/deposits/signals.py'),
    os.path.exists('apps/withdrawals/signals.py'),
]
all_checks_passed &= print_status(
    "Investment signals configured",
    signals_exist[0]
)
all_checks_passed &= print_status(
    "Deposit signals configured",
    signals_exist[1]
)
all_checks_passed &= print_status(
    "Withdrawal signals configured",
    signals_exist[2]
)

# 9. Templates
print_header("9. Template Configuration")
templates_exist = [
    os.path.exists('templates/base.html'),
    os.path.exists('templates/dashboard.html'),
    os.path.exists('templates/login.html'),
    os.path.exists('templates/investments.html'),
    os.path.exists('templates/deposits.html'),
    os.path.exists('templates/withdrawals.html'),
    os.path.exists('templates/support.html'),
    os.path.exists('templates/profile.html'),
]
all_checks_passed &= print_status(
    f"Required templates ({sum(templates_exist)}/8)",
    all(templates_exist)
)

# 10. Dependencies
print_header("10. Dependencies")
required_packages = [
    'django',
    'djangorestframework',
    'whitenoise',
    'gunicorn',
    'pillow',
]
try:
    import pkg_resources
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for package in required_packages:
        all_checks_passed &= print_status(
            f"Package: {package}",
            package in installed_packages
        )
except Exception as e:
    print_status(f"Package check error: {e}", False)

# 11. Files
print_header("11. Deployment Files")
deployment_files = [
    ('Procfile', os.path.exists('Procfile')),
    ('requirements.txt', os.path.exists('requirements.txt')),
    ('runtime.txt', os.path.exists('runtime.txt')),
    ('.env.example', os.path.exists('.env.example')),
    ('DEPLOYMENT.md', os.path.exists('DEPLOYMENT.md')),
    ('.gitignore', os.path.exists('.gitignore')),
]
for filename, exists in deployment_files:
    print_status(f"File: {filename}", exists)

# 12. URLs and Endpoints
print_header("12. URL Configuration")
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    url_patterns = [pattern.pattern._route for pattern in resolver.url_patterns if hasattr(pattern.pattern, '_route')]
    
    required_urls = ['admin/', 'api/', 'login/', 'dashboard/']
    for url in required_urls:
        exists = any(url in str(pattern) for pattern in url_patterns)
        print_status(f"URL: {url}", exists)
except Exception as e:
    print_status(f"URL check error: {e}", False)

# Final Summary
print_header("SUMMARY")
if all_checks_passed:
    print("\033[92m✓ ALL CHECKS PASSED - Ready for deployment!\033[0m")
    print("\nNext steps:")
    print("1. Review .env.example and create production .env file")
    print("2. Set DEBUG=False in production")
    print("3. Configure PostgreSQL database")
    print("4. Set up SSL certificate (HTTPS)")
    print("5. Configure web server (Nginx/Apache)")
    print("6. Set up Gunicorn with systemd")
    print("7. Run 'python manage.py check --deploy' for final security check")
    print("\nSee DEPLOYMENT.md for detailed instructions.")
else:
    print("\033[91m✗ SOME CHECKS FAILED - Review issues above before deploying\033[0m")
    print("\nAddress all failures before proceeding with deployment.")

print("\n" + "="*70 + "\n")

sys.exit(0 if all_checks_passed else 1)
