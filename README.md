# Tesla Investment Platform

A comprehensive Django-based investment platform with Tesla-inspired dark theme, user authentication, investment plans, deposits, withdrawals, and support system.

## 🚀 Features

### User Side
- **Authentication**: Secure registration and login with email
- **Dashboard**: View balance, investments, and earnings with real-time updates
- **Deposit Management**: Submit crypto deposits with proof
- **Investment Plans**: Browse and subscribe to investment plans with automatic ROI crediting
- **Withdrawals**: Request fund withdrawals with automatic balance handling
- **Support System**: Create tickets and communicate with admin

### Admin Side (Django Admin)
- **User Management**: Manage user balances and accounts
- **Deposit Approval**: Approve deposits with automatic balance updates
- **Support Management**: Reply to user tickets inline
- **Investment Plans**: Create and manage investment plans
- **Withdrawal Processing**: Approve/reject with automatic refund on rejection

### Automated Features
- ✅ **Automatic Balance Updates**: Deposits auto-credit on approval
- ✅ **Smart Refunds**: Rejected withdrawals auto-refund balance
- ✅ **ROI Crediting**: Completed investments automatically credit earnings + principal
- ✅ **Duplicate Prevention**: Status-change detection prevents double-credits
- ✅ **Total Earnings Tracking**: Dashboard tracks cumulative ROI earnings

## 🛠 Technical Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Frontend**: Tailwind CSS (Tesla dark theme), Alpine.js, Vanilla JavaScript
- **Database**: SQLite (default), PostgreSQL (production)
- **Authentication**: Token-based + Session authentication
- **Security**: CSRF protection, JWT support, HTTPS ready
- **Static Files**: WhiteNoise with compression
- **Deployment**: Gunicorn + Nginx ready

## 📋 Prerequisites

- Python 3.14.0
- pip and virtualenv
- PostgreSQL (for production)
- Nginx (for production deployment)

## 📦 Installation

### Development Setup

1. **Clone the Repository**
   ```bash
   git clone <your-repo>
   cd prodig
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver 8001
   ```

Access at `http://127.0.0.1:8001`

### Pre-Deployment Check

Run the deployment readiness checker:
```bash
python check_deployment.py
```

This validates:
- ✅ Environment configuration
- ✅ Database connectivity
- ✅ Static files collection
- ✅ Security settings
- ✅ Required dependencies
- ✅ Signal handlers
- ✅ Template files

## 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive production deployment guide.

Quick production checklist:
1. Set `DEBUG=False` in .env
2. Configure PostgreSQL database
3. Set strong `SECRET_KEY`
4. Update `ALLOWED_HOSTS`
5. Enable SSL/HTTPS
6. Configure Gunicorn + Nginx
7. Run `python manage.py check --deploy`

## API Documentation

### Authentication Endpoints
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login user
- `POST /api/users/logout/` - Logout user
- `GET /api/users/me/` - Get current user profile

### Investment Endpoints
- `GET /api/investments/plans/` - Get all investment plans
- `GET /api/investments/my-investments/` - Get user investments
- `POST /api/investments/my-investments/subscribe/` - Subscribe to plan

### Deposit Endpoints
- `GET /api/deposits/wallets/` - Get crypto wallets
- `GET /api/deposits/` - Get user deposits
- `POST /api/deposits/` - Submit new deposit

### Withdrawal Endpoints
- `GET /api/withdrawals/` - Get user withdrawals
- `POST /api/withdrawals/request_withdrawal/` - Request withdrawal

### Support Endpoints
- `GET /api/support/tickets/` - Get support tickets
- `POST /api/support/tickets/` - Create ticket
- `POST /api/support/tickets/{id}/add_reply/` - Add reply

## Database Models

### CustomUser
- Email, username, password
- Balance, total_invested, total_earnings
- Profile information

### InvestmentPlan
- Name, description
- ROI percentage, duration
- Min/max investment amounts

### UserInvestment
- User, plan, amount
- Status, dates, returns

### CryptoWallet
- Cryptocurrency type
- Wallet address

### Deposit
- User, amount, cryptocurrency
- Proof type and content
- Status (pending/approved/rejected)

### Withdrawal
- User, amount, cryptocurrency
- Wallet address, status
- **Signal**: Auto-refunds on rejection

### SupportTicket & SupportReply
- Priority, status, category
- Admin inline replies
- User-admin communication

## 🎯 Automated Transaction Flow

### Deposit Flow
1. User submits deposit with proof
2. Admin reviews in Django admin
3. Admin approves → **Signal auto-credits balance**
4. Duplicate prevention via `approved_at` timestamp

### Withdrawal Flow
1. User requests withdrawal (balance deducted)
2. Admin reviews request
3. If rejected → **Signal auto-refunds balance**
4. Duplicate prevention via status change detection

### Investment Flow
1. User subscribes to plan (balance deducted)
2. Investment becomes active
3. Admin completes investment → **Signal credits:**
   - Principal amount back to balance
   - ROI earnings to balance
   - Updates `total_earnings` field
4. User can cancel active investment → **Signal refunds amount**
5. Duplicate prevention via `earned` field check

## 🌐 API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login (returns token)
- `POST /api/users/logout/` - Logout
- `GET /api/users/me/` - Current user profile

### Investments
- `GET /api/investments/plans/` - List investment plans
- `GET /api/investments/my-investments/` - User's investments
- `POST /api/investments/my-investments/subscribe/` - Subscribe to plan
- `POST /api/investments/my-investments/cancel_investment/` - Cancel investment

### Deposits
- `GET /api/deposits/wallets/` - Crypto wallet addresses
- `GET /api/deposits/my_deposits/` - User's deposits
- `POST /api/deposits/` - Submit new deposit

### Withdrawals
- `GET /api/withdrawals/my-withdrawals/` - User's withdrawals
- `POST /api/withdrawals/request_withdrawal/` - Request withdrawal

### Support
- `GET /api/support/tickets/` - List user tickets
- `POST /api/support/tickets/` - Create ticket
- `GET /api/support/tickets/{id}/` - Ticket details with replies
- `POST /api/support/tickets/{id}/add_reply/` - Add reply

## 🔧 Admin Panel

Access: `http://yourdomain.com/admin/`

### Key Features
- **User Management**: Edit balances, total_invested, total_earnings
- **Deposit Approval**: Inline actions, auto-balance update
- **Investment Tracking**: View all active/completed investments
- **Withdrawal Processing**: Approve with proof, reject with auto-refund
- **Support Tickets**: Inline reply system with admin indicator
- **Investment Plans**: Create plans with ROI % and duration

### Admin Credentials
Set during deployment with `python manage.py createsuperuser`

## 🚨 Troubleshooting

### Dashboard not showing updated earnings
1. Check browser console for JavaScript errors
2. Verify API endpoint returns correct data: `/api/users/me/`
3. Hard refresh: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)

### Balance not updating after approval
1. Check Django admin logs
2. Verify signal files exist:
   - `apps/deposits/signals.py`
   - `apps/withdrawals/signals.py`
   - `apps/investments/signals.py`
3. Check apps.py imports signals in `ready()` method

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database errors
```bash
python manage.py migrate
python manage.py check
```

## 📝 Development Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver 8001

# Django shell
python manage.py shell

# Check deployment readiness
python check_deployment.py

# Security check
python manage.py check --deploy
```

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Complete production deployment guide
- **[FRONTEND_COMPLETE.md](FRONTEND_COMPLETE.md)**: Frontend implementation details
- **[SSR_MIGRATION.md](SSR_MIGRATION.md)**: Server-side rendering notes
- **[SYSTEM_STATUS.md](SYSTEM_STATUS.md)**: System status and features

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

Proprietary - All rights reserved © 2024-2025

## 🙋 Support

- **In-App**: Use the support ticket system
- **Admin**: Login to Django admin for backend management
- **Documentation**: See DEPLOYMENT.md for detailed guides

---

**Built with Django 4.2.7 | Styled with Tesla-inspired design | Ready for Production** 🚀

## Project Structure

```
prodig/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── apps/
│   ├── users/
│   ├── investments/
│   ├── deposits/
│   ├── withdrawals/
│   └── support/
├── templates/
│   ├── base.html
│   ├── login.html
│  🔧 Configuration

### Environment Variables (.env)

**Development:**
```env
DEBUG=True
SECRET_KEY=development-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
```

**Production:**
```env
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=investment_platform
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_HOST=localhost
DB_PORT=5432
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## 🧪 Testing

### Run Pre-Deployment Checks
```bash
python check_deployment.py
```

### Django Deployment Check
```bash
python manage.py check --deploy
```

### Test Individual Components
```bash
# Test investment completion and earnings
python test_complete_inv.py

# Test database connectivity
python check_db.py
```

## 📁 Project Structure

```
prodig/
├── manage.py
├── requirements.txt
├── Procfile                    # Heroku/deployment
├── runtime.txt                 # Python version
├── DEPLOYMENT.md              # Deployment guide
├── check_deployment.py        # Pre-deployment validator
├── config/
│   ├── settings.py            # Base settings
│   ├── settings_production.py # Production settings
│   ├── urls.py
│   ├── wsgi.py
│   └── context_processors.py
├── apps/
│   ├── users/                 # User management
│   │   ├── models.py          # CustomUser model
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── investments/           # Investment system
│   │   ├── models.py          # InvestmentPlan, UserInvestment
│   │   ├── signals.py         # Auto ROI crediting
│   │   └── views.py
│   ├── deposits/              # Deposit handling
│   │   ├── models.py          # Deposit, CryptoWallet
│   │   ├── signals.py         # Auto balance update
│   │   └── views.py
│   ├── withdrawals/           # Withdrawal system
│   │   ├── models.py          # Withdrawal
│   │   ├── signals.py         # Auto refund
│   │   └── views.py
│   └── support/               # Support tickets
│       ├── models.py          # SupportTicket, SupportReply
│       ├── admin.py           # Inline admin replies
│       └── views.py
├── templates/                 # HTML templates (Tesla theme)
│   ├── base.html              # Master template
│   ├── dashboard.html         # Main dashboard
│   ├── investments.html       # Investment page
│   ├── deposits.html          # Deposit page
│   ├── withdrawals.html       # Withdrawal page
│   └── support.html           # Support page
└── static/                    # Frontend assets
    ├── css/
    │   └── tesla.css          # Tesla dark theme
    └── js/
        ├── main.js            # API utilities
        ├── dashboard.js       # Dashboard logic
        ├── investments.js     # Investment logic
        ├── deposits.js        # Deposit logic
        ├── withdrawals.js     # Withdrawal logic
        └── support.js         # Support logic
```

## 🔐 Security Features

- **CSRF Protection**: All forms protected
- **Token Authentication**: Secure API endpoints
- **Password Hashing**: Django PBKDF2 with SHA256
- **SSL/HTTPS Support**: Production-ready configuration
- **Input Validation**: Server-side validation
- **XSS Protection**: Template auto-escaping
- **Secure Cookies**: HTTPOnly, Secure, SameSite
- **SQL Injection Protection**: ORM parameterized queries

## 🎨 UI/UX Features

- **Tesla Dark Theme**: Professional black & gray design
- **Mobile Responsive**: Works on all device sizes
- **Alpine.js**: Interactive hamburger menu
- **Real-time Updates**: JavaScript fetches live data
- **Status Badges**: Color-coded transaction statuses
- **Modal Dialogs**: Support ticket details
- **Form Validation**: Client + server side

## 📊 Database Models
python manage.py makemigrations
python manage.py migrate
```

### Load Sample Data
Create sample investment plans and crypto wallets through the admin panel.

## Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Production Settings
- Set `DEBUG=False`
- Update `SECRET_KEY` to strong value
- Configure `ALLOWED_HOSTS`
- Enable `SECURE_SSL_REDIRECT=True`
- Setup PostgreSQL database
- Use environment variables for sensitive data

## Support

For issues or questions, create a support ticket through the platform.

## License

Proprietary - All rights reserved
