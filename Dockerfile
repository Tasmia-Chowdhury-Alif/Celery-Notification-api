# Use official Python image as base
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project code
COPY . .

# Expose port 8000 (Django default)
EXPOSE 8000

# Run migrations and start server
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn notification_system.wsgi:application --bind 0.0.0.0:8000"]