"""
Celery Tasks for Notifications
------------------------------
Handles background email sending with retry logic.
All times are in UTC.
"""

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Notification

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id):
    """
    Send email notification at scheduled UTC time.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        current_time = timezone.now()  # UTC

        logger.info(f"🚀 Starting notification task | ID: {notification_id} | Title: {notification.title}")
        logger.info(f"📅 Scheduled Time (UTC): {notification.scheduled_time}")
        logger.info(f"⏰ Current Time (UTC)  : {current_time}")
        logger.info(f"📧 Recipient: {notification.user.email} | Status: {notification.status} | Retry Count: {notification.retry_count}")

        # Safety checks
        if notification.status == 'permanent_failed':
            logger.warning(f"⛔ Skipping permanently failed notification {notification_id}")
            return "Skipped"

        if notification.scheduled_time > current_time + timezone.timedelta(minutes=5):
            logger.warning(f"⚠️ Notification {notification_id} is being processed too early")

        # Send Email
        send_mail(
            subject=notification.title,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
            fail_silently=False,
        )

        # Mark as sent
        notification.status = 'sent'
        notification.save()

        logger.info(f"✅ SUCCESS - Email sent to {notification.user.email}")
        logger.info(f"📊 Final Status: Sent | ID: {notification_id} | Sent At (UTC): {current_time}")

        return "Success"

    except Exception as exc:
        # Refresh notification object
        notification = Notification.objects.get(id=notification_id)
        notification.retry_count += 1
        current_time = timezone.now()

        logger.error(f"❌ FAILED - Notification ID: {notification_id}")
        logger.error(f"📅 Scheduled (UTC): {notification.scheduled_time} | Attempt Time (UTC): {current_time}")
        logger.error(f"🔁 Attempt {notification.retry_count}/3 | Error: {str(exc)}")

        if notification.retry_count >= 3:
            notification.status = 'permanent_failed'
            notification.save()
            logger.error(f"🚫 Notification {notification_id} marked as PERMANENT_FAILED")
            return "Permanent Failed"
        else:
            notification.status = 'failed'
            notification.save()
            # logger.warning(f"🔄 Retrying notification {notification_id}...")
            # raise self.retry(exc=exc)