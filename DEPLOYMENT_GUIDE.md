# 🚀 Django Email Template - Deployment Guide

## Option 1: PythonAnywhere (Recommended for Testing)

### Step 1: Create Account
1. Go to: https://www.pythonanywhere.com/registration/register/beginner/
2. Sign up (Free account)
3. Verify email

### Step 2: Upload Code
```bash
# On PythonAnywhere Bash Console
git clone https://github.com/proalamin/Email_tamplate.git
cd Email_tamplate
```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 emailenv
pip install -r requirements.txt
```

### Step 4: Configure Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Python version: 3.10
5. Set paths:
   - Source code: `/home/YOUR_USERNAME/Email_tamplate`
   - Working directory: `/home/YOUR_USERNAME/Email_tamplate`
   - Virtualenv: `/home/YOUR_USERNAME/.virtualenvs/emailenv`

### Step 6: Edit WSGI file
```python
import sys
import os

path = '/home/YOUR_USERNAME/Email_tamplate'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'email_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 7: Configure Static Files
In Web tab:
- URL: `/static/`
- Directory: `/home/YOUR_USERNAME/Email_tamplate/staticfiles`

Run:
```bash
python manage.py collectstatic
```

### Step 8: Update settings.py
```python
ALLOWED_HOSTS = ['YOUR_USERNAME.pythonanywhere.com']
DEBUG = False
```

### Step 9: Reload Web App
Click "Reload" button in Web tab

### Your site will be live at:
`https://YOUR_USERNAME.pythonanywhere.com`

---

## Option 2: Railway.app (Recommended for Production)

### Step 1: Prepare Project

1. Create `Procfile`:
```
web: gunicorn email_project.wsgi --log-file -
```

2. Update `requirements.txt`:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
echo "whitenoise==6.6.0" >> requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt
```

3. Update `settings.py`:
```python
import os
import dj_database_url

# Add whitenoise to middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Allowed hosts
ALLOWED_HOSTS = ['*']  # Update with your domain later
```

### Step 2: Deploy to Railway

1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `Email_tamplate` repository
6. Railway will auto-detect Django and deploy!

### Step 3: Add PostgreSQL Database
1. In your project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically set DATABASE_URL

### Step 4: Run Migrations
In Railway dashboard:
1. Go to your service
2. Click "Settings" → "Deploy"
3. Add custom start command:
```bash
python manage.py migrate && gunicorn email_project.wsgi
```

### Step 5: Set Environment Variables
In Railway dashboard → Variables:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
```

### Your site will be live at:
`https://your-app.railway.app`

---

## Option 3: Render.com

### Step 1: Create `render.yaml`
```yaml
services:
  - type: web
    name: email-template
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
    startCommand: gunicorn email_project.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: DATABASE_URL
        fromDatabase:
          name: email-db
          property: connectionString

databases:
  - name: email-db
    plan: free
```

### Step 2: Deploy
1. Go to: https://render.com/
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Render will auto-deploy!

---

## 🔒 Security Checklist Before Deployment

### 1. Update settings.py
```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Generate new secret key
SECRET_KEY = 'your-new-secret-key-here'

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Create .env file
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
```

### 3. Update .gitignore
```
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
```

### 4. Use environment variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## 📊 Comparison Table

| Platform | Free Tier | Database | Custom Domain | Auto-Deploy | Best For |
|----------|-----------|----------|---------------|-------------|----------|
| **PythonAnywhere** | ✅ Always Free | MySQL/PostgreSQL | ❌ Paid | ❌ Manual | Testing |
| **Railway** | $5/month credit | PostgreSQL | ✅ Free | ✅ GitHub | Production |
| **Render** | 750 hrs/month | PostgreSQL (90 days) | ✅ Free | ✅ GitHub | Production |
| **Vercel** | Unlimited | ❌ External | ✅ Free | ✅ GitHub | Frontend |

---

## 🎯 Quick Start Commands

### For PythonAnywhere:
```bash
git clone https://github.com/proalamin/Email_tamplate.git
cd Email_tamplate
mkvirtualenv emailenv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### For Railway/Render:
```bash
# Add to requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt
echo "whitenoise==6.6.0" >> requirements.txt
echo "dj-database-url==2.1.0" >> requirements.txt

# Create Procfile
echo "web: gunicorn email_project.wsgi" > Procfile

# Commit and push
git add .
git commit -m "Prepare for deployment"
git push origin main
```

---

## 🆘 Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic --no-input
```

### Issue: Database connection error
Check DATABASE_URL environment variable

### Issue: 502 Bad Gateway
Check logs:
```bash
# PythonAnywhere: Error log in Web tab
# Railway: View logs in dashboard
# Render: View logs in dashboard
```

### Issue: Email not sending
Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in environment variables

---

## 📞 Support

- PythonAnywhere: https://help.pythonanywhere.com/
- Railway: https://docs.railway.app/
- Render: https://render.com/docs

---

## ✅ Post-Deployment Checklist

- [ ] Site is accessible
- [ ] Admin panel works (/admin)
- [ ] Can upload Excel files
- [ ] Can add email accounts
- [ ] Can send test email
- [ ] Static files loading
- [ ] Database working
- [ ] Email accounts saving
- [ ] Priority system working

---

**Good luck with deployment! 🚀**
