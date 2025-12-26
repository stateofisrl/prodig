# Render Deployment - Quick Start

## 🚀 Deploy to Render in 5 Minutes

### Cost: $14/month ($7 web service + $7 PostgreSQL)

---

## ✅ Files Ready for Render:
- ✅ `render.yaml` - Configuration file
- ✅ `build.sh` - Build script  
- ✅ `requirements.txt` - Updated with dj-database-url
- ✅ `config/settings.py` - DATABASE_URL support added

---

## 📝 Quick Steps:

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Deploy to Render"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### 2. Deploy on Render
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repo
4. Render detects `render.yaml` automatically
5. Select **Standard Plan ($7/month)** for both services
6. Click **"Apply"**

### 3. Set Environment Variables (Auto-configured)
Render will set these from `render.yaml`:
- `SECRET_KEY` (auto-generated)
- `DEBUG=False`
- `DATABASE_URL` (from PostgreSQL)
- `ALLOWED_HOSTS` (your-app.onrender.com)
- All security settings

### 4. Create Superuser
After deployment, click **"Shell"** in dashboard:
```bash
python manage.py createsuperuser
```

### 5. Access Your Site
- **Frontend**: https://your-app-name.onrender.com
- **Admin**: https://your-app-name.onrender.com/admin/

---

## 💰 Pricing

| Service | Plan | Cost |
|---------|------|------|
| Web Service | Standard (512 MB RAM) | $7/mo |
| PostgreSQL | Standard (1 GB storage) | $7/mo |
| **Total** | | **$14/mo** |

### Included:
✅ Automatic SSL (HTTPS)
✅ Daily backups (7 days)
✅ Auto-deploy from Git
✅ Custom domain support
✅ 24/7 uptime

---

## 🔧 Important Files

### render.yaml
```yaml
services:
  - type: web
    name: tesla-investment-platform
    plan: standard  # $7/month
    
databases:
  - name: tesla-investment-db
    plan: standard  # $7/month
```

### build.sh
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## 🚨 Before Deploying

1. **Make build.sh executable**:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   ```

2. **Update ALLOWED_HOSTS after deployment**:
   Add your Render URL to environment variables:
   ```
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

3. **Generate SECRET_KEY**:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Add to Render environment variables (or let Render auto-generate)

---

## 📊 After Deployment

### Configure via Admin:
1. Login to /admin/
2. Create investment plans
3. Add crypto wallet addresses
4. Test all features

### Monitor:
- Logs: Render Dashboard → Your Service → Logs
- Metrics: Dashboard shows CPU, RAM, response times
- Deployments: Auto-deploy on every git push

---

## 🆘 Troubleshooting

### Build fails?
- Check build.sh is executable: `git ls-files -s build.sh`
- Should show `100755`, not `100644`

### Can't connect to database?
- Verify DATABASE_URL in environment variables
- Check PostgreSQL service is running

### Static files not loading?
- Verify build.sh runs collectstatic
- Check WhiteNoise is in MIDDLEWARE

---

## 📚 Full Documentation

See **RENDER_DEPLOYMENT.md** for:
- Detailed step-by-step guide
- Custom domain setup
- Database backups
- Security checklist
- Monitoring & logs
- Cost optimization

---

## ⚡ Auto-Deploy

Push changes to deploy:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Render automatically deploys!
```

---

**Ready in 5 minutes!** 🚀

Total Setup Time: ~5-10 minutes
Monthly Cost: $14
Includes: SSL, Backups, Auto-deploy
