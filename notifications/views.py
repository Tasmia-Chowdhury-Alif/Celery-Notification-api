"""
Notification Views
------------------
REST API endpoints for managing scheduled notifications.
All datetime handling is in UTC.
"""

import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationRetrySerializer, NotificationSerializer
from .tasks import send_notification_task
from django.utils import timezone

logger = logging.getLogger(__name__)


class NotificationListCreateView(generics.ListCreateAPIView):
    """
    GET: List all notifications of the authenticated user.
    POST: Create a new scheduled notification (in UTC).
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only notifications belonging to the current user."""
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save notification and schedule Celery task with ETA in UTC.
        """
        notification = serializer.save()

        now = timezone.now()  # UTC
        if notification.scheduled_time > now:
            send_notification_task.apply_async(
                args=[notification.id],
                eta=notification.scheduled_time,   # Must be UTC
            )
            logger.info(f"Notification {notification.id} scheduled successfully at (UTC): {notification.scheduled_time}")
        else:
            # Fallback (should not reach here due to validation)
            notification.status = 'permanent_failed'
            notification.save()

        return notification


class NotificationRetryView(generics.GenericAPIView):
    """
    POST: Retry a failed notification (max 3 attempts).
    """
    serializer_class = NotificationRetrySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=404)

        if notification.status != 'failed':
            return Response({"detail": "Only failed notifications can be retried."}, status=400)

        if notification.retry_count >= 3:
            return Response({"detail": "Maximum retry attempts (3) reached."}, status=400)

        # Prepare for retry
        notification.status = 'pending'
        notification.retry_count += 1
        notification.save()

        # Re-schedule with Celery (immediate retry)
        send_notification_task.delay(notification.id)

        return Response({
            "detail": "Notification retry scheduled successfully.",
            "retry_count": notification.retry_count
        }, status=200)