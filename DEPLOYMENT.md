# Deployment Guide

## Tesla Investment Platform - Production Deployment

### Prerequisites

- Python 3.14.0
- PostgreSQL (recommended for production)
- Redis (optional, for Celery)
- Web server (Nginx/Apache)

### Step 1: Environment Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd prodig
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update `.env` with your production values:
   - Generate a strong SECRET_KEY
   - Set DEBUG=False
   - Add your domain to ALLOWED_HOSTS
   - Configure database credentials
   - Enable security settings

### Step 2: Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE your_database_name;
CREATE USER your_database_user WITH PASSWORD 'your_password';
ALTER ROLE your_database_user SET client_encoding TO 'utf8';
ALTER ROLE your_database_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_database_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_database_user;
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

### Step 3: Static Files

Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Step 4: Security Checklist

Run Django's deployment checklist:
```bash
python manage.py check --deploy
```

### Step 5: Web Server Configuration

#### Gunicorn (Application Server)

Start Gunicorn:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

#### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /path/to/prodig/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/prodig/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 6: SSL Certificate (HTTPS)

Install Let's Encrypt SSL:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Step 7: Process Manager (Systemd)

Create `/etc/systemd/system/prodig.service`:
```ini
[Unit]
Description=Tesla Investment Platform
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/prodig
Environment="PATH=/path/to/prodig/venv/bin"
ExecStart=/path/to/prodig/venv/bin/gunicorn --workers 3 --bind unix:/path/to/prodig/prodig.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable prodig
sudo systemctl start prodig
sudo systemctl status prodig
```

### Step 8: Monitoring & Logs

View application logs:
```bash
sudo journalctl -u prodig -f
```

### Production Features

✅ **Security**
- HTTPS enforced
- CSRF protection
- Session security
- Password validation
- XSS protection

✅ **Performance**
- WhiteNoise for static files
- Compressed static assets
- Database query optimization
- Token authentication

✅ **Reliability**
- Automated balance updates
- Duplicate prevention
- Signal-based transactions
- Error handling

### API Endpoints

- `/api/users/` - User management
- `/api/investments/` - Investment operations
- `/api/deposits/` - Deposit handling
- `/api/withdrawals/` - Withdrawal requests
- `/api/support/` - Support tickets
- `/admin/` - Admin interface

### Default Credentials

**Admin Account:**
- Email: admin@example.com
- Password: (set during deployment)

**Important:** Change all default passwords immediately after deployment!

### Troubleshooting

**Static files not loading:**
```bash
python manage.py collectstatic --clear --noinput
```

**Database connection errors:**
- Check PostgreSQL is running
- Verify credentials in .env
- Ensure database exists

**Permission errors:**
- Check file ownership: `chown -R user:www-data /path/to/prodig`
- Check file permissions: `chmod -R 755 /path/to/prodig`

### Backup Strategy

**Database backup:**
```bash
pg_dump your_database_name > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Media files backup:**
```bash
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### Maintenance

**Update dependencies:**
```bash
pip install -U -r requirements.txt
```

**Apply new migrations:**
```bash
python manage.py migrate
```

**Restart service:**
```bash
sudo systemctl restart prodig
```

### Support

For issues or questions, refer to:
- Django documentation: https://docs.djangoproject.com/
- DRF documentation: https://www.django-rest-framework.org/
- Project README: README.md

---

**Last Updated:** December 25, 2025
