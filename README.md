# Celery Notification API

A robust **Django + Celery** based background job notification system that allows users to schedule, manage, and track notifications with retry logic and proper failure handling.

## ✨ Features

- **User Authentication** (JWT + Djoser)
- **Create & Schedule Notifications** with timezone support
- **Background Task Processing** using Celery
- **Retry Logic** with max 3 attempts
- **Notification Status Tracking** (Pending, Sent, Failed, Permanently Failed)
- **Production Ready** setup with external services
- **Docker Support** with multi-environment configuration
- **Comprehensive Error Handling** and logging

## 🛠 Tech Stack

- **Backend**: Django + Django REST Framework
- **Task Queue**: Celery
- **Database**: PostgreSQL (Neon in Production)
- **Cache/Broker**: Redis (Upstash in Production)
- **Containerization**: Docker + Docker Compose
- **API Documentation**: drf-spectacular (Swagger UI)
- **Authentication**: JWT + Djoser

## 🚀 Quick Start

### Development
```bash
docker compose up --build
