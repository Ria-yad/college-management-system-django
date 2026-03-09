# Django College Management System - Deployment Guide

## Production Checklist

### 1. Security Configuration

#### `settings.py` Updates:
```python
# Set DEBUG to False
DEBUG = False

# Generate a secure SECRET_KEY
SECRET_KEY = 'your-very-long-secure-random-string-here'

# Configure allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-server-ip']

# CSRF and CORS settings
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURITY_HSTS_SECONDS = 31536000
SECURITY_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}

# Allowed HTTP only for admin if needed
ALLOWED_INCLUDE_HOSTS = ["yourdomain.com"]
```

### 2. Database Setup

#### Option A: PostgreSQL (Recommended)
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'college_erp_db',
        'USER': 'college_user',
        'PASSWORD': 'strong-password-here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Option B: MySQL
```bash
# Install MySQL adapter
pip install mysqlclient

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'college_erp_db',
        'USER': 'college_user',
        'PASSWORD': 'strong-password-here',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Static and Media Files

#### Configure Static Files:
```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For production, use AWS S3 or similar
# Install: pip install django-storages boto3
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
    },
}
```

#### Collect Static Files:
```bash
python manage.py collectstatic --noinput
```

### 4. Email Configuration

#### Configure Email Backend (Gmail Example):
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Passwords, not main password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### 5. Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/college_erp.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
```

### 6. Web Server Setup - Gunicorn

#### Install Gunicorn:
```bash
pip install gunicorn
```

#### Create `gunicorn_config.py`:
```python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management_project.settings")

bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
max_requests = 100
max_requests_jitter = 10
timeout = 60
keepalive = 2
log_level = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```

#### Run Gunicorn:
```bash
gunicorn -c gunicorn_config.py student_management_project.wsgi:application
```

### 7. Nginx Configuration

#### Install Nginx:
```bash
sudo apt-get install nginx
```

#### Create `/etc/nginx/sites-available/college-erp`:
```nginx
upstream college_erp {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    client_max_body_size 10M;

    location / {
        proxy_pass http://college_erp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/project/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /path/to/project/media/;
        expires 7d;
    }
}

# HTTPS Redirect (after SSL setup)
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    # ... rest of config
}
```

#### Enable Site:
```bash
sudo ln -s /etc/nginx/sites-available/college-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL/TLS Setup with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### 9. Systemd Service File

#### Create `/etc/systemd/system/college-erp.service`:
```ini
[Unit]
Description=College ERP Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/college_management_project
EnvironmentFile=/path/to/.env
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    student_management_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable college-erp
sudo systemctl start college-erp
sudo systemctl status college-erp
```

### 10. Environment Variables (.env file)

```ini
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/college_erp
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### Load Environment Variables:
```bash
pip install python-decouple
```

```python
# settings.py
from decouple import config, Csv

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

### 11. Database Migration in Production

```bash
# Before deployment
python manage.py makemigrations
python manage.py migrate --plan

# On production server
python manage.py migrate
python manage.py collectstatic --noinput
```

### 12. Backup Strategy

#### Database Backup Script:
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/path/to/backups"
DATE=$(date +\%Y\%m\%d_\%H\%M\%S)

# PostgreSQL
pg_dump -U college_user college_erp_db > "$BACKUP_DIR/db_backup_$DATE.sql"

# Compress
gzip "$BACKUP_DIR/db_backup_$DATE.sql"

# Keep only last 7 days
find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +7 -delete

# Upload to S3 (optional)
aws s3 cp "$BACKUP_DIR/db_backup_$DATE.sql.gz" s3://your-bucket/backups/
```

#### Schedule Backups with Cron:
```bash
# Add to crontab -e
0 2 * * * /path/to/backup.sh  # Run daily at 2 AM
```

### 13. Monitoring and Maintenance

#### Health Check Endpoint (Optional):
```python
# urls.py
path('health/', lambda request: JsonResponse({'status': 'ok'}), name='health')
```

#### Monitor with Nginx:
```nginx
location /health/ {
    proxy_pass http://college_erp;
    access_log off;
}
```

#### Log Monitoring:
```bash
tail -f /var/log/django/college_erp.log
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## Production Deployment Steps

1. **Clone Repository** on production server
2. **Create Virtual Environment** and install dependencies
3. **Configure `.env` file** with production settings
4. **Run Migrations** with production database
5. **Collect Static Files** for production
6. **Setup Gunicorn** service
7. **Configure Nginx** as reverse proxy
8. **Setup SSL/TLS** with Let's Encrypt
9. **Enable Systemd Service** for auto-start
10. **Setup Monitoring** and logging
11. **Configure Backups** and restore procedures
12. **Test End-to-End** workflows

---

## Performance Optimization

### Enable Query Optimization:
```python
# settings.py
DEBUG_PROPAGATE_EXCEPTIONS = True
```

### Use Database Indexes:
```python
# models.py
class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_index=True)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, db_index=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['admin', 'course_id']),
        ]
```

### Use Caching:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## Troubleshooting

### 502 Bad Gateway
- Check if Gunicorn is running: `systemctl status college-erp`
- Check Nginx error logs: `tail -f /var/log/nginx/error.log`

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Ensure `STATIC_ROOT` path is correct

### Database Connection Issues
- Verify database credentials in `.env`
- Check if database service is running

---

## Monitoring Commands

```bash
# Check application logs
journalctl -u college-erp -f

# Monitor system resources
htop

# Check Nginx status
sudo systemctl status nginx

# Test Nginx config
sudo nginx -t

# Reload Nginx safely
sudo systemctl reload nginx
```

---

**Last Updated**: February 23, 2026
**Django Version**: 6.0.2
