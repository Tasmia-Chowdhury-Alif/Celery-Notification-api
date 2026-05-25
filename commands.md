# 📋 Project Commands Guide

**Celery_Notification_API** - Django + Celery Background Notification System


## 🛠 Local Development Setup

### 1. Create & Activate Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
source .venv/Scripts/activate

# Activate (Linux / Mac)
# source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Server with Gunicorn (Production-like)
```bash
gunicorn notification_system.wsgi:application --bind 0.0.0.0:8000
```


## 🐳 Docker Commands (Recommended)

### Start the Project
```bash
# Build and start containers
docker-compose up --build

# Start in background (detached mode)
docker-compose up --build -d
```

### Stop & Cleanup
```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (⚠️ Deletes local database data)
docker-compose down -v
```

### Restart & Rebuild
```bash
# Restart with full rebuild
docker-compose up --build --force-recreate

# Restart only specific service (example: web)
docker-compose restart web
```


## 🔧 Django Management Commands

```bash
# Run Migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Create Superuser
docker-compose exec web python manage.py createsuperuser

# Collect Static Files
docker-compose exec web python manage.py collectstatic --noinput

# Django Shell
docker-compose exec web python manage.py shell
```


## 📊 Celery & Logging

```bash
# View real-time logs
docker-compose logs -f

# View only Celery worker logs
docker-compose logs -f celery

# Restart Celery worker only
docker-compose restart celery
```


## 🔄 Other Useful Commands

```bash
# Check running containers
docker-compose ps

# Enter into web container shell
docker-compose exec web bash

# Rebuild project from scratch
docker-compose down -v && docker-compose up --build
```


**Tip**: Always check container logs if something goes wrong:
```bash
docker-compose logs -f web
```


**Note**: This project uses local PostgreSQL in development and external services (Neon + Upstash) in production via environment variables.

