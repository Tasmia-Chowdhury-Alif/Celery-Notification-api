"""
Notification Serializers
------------------------
All datetime fields are handled in UTC only.
Clients must send scheduled_time in UTC. 
All scheduled_time must be provided in UTC by the frontend.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing notifications.
    
    Note for Frontend:
        - Always send scheduled_time in UTC (recommended: ISO format with Z).
        - Example: "2026-05-25T14:30:00Z"
    """
    scheduled_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        input_formats=['%Y-%m-%d %H:%M:%S', 'iso-8601'],
        help_text="Scheduled time must be in UTC. Frontend must convert local time to UTC. Must be at least 30 seconds in the future."
    )

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'scheduled_time', 'status', 'retry_count', 'created_at']
        read_only_fields = ['status', 'retry_count', 'created_at']

    def validate_scheduled_time(self, value):
        """
        Ensure the scheduled time is in the future (UTC comparison).
        """
        # Force UTC awareness if client sends naive datetime
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.utc)

        if value <= timezone.now() + timezone.timedelta(seconds=30):
            raise serializers.ValidationError(
                "Scheduled time must be at least 30 seconds in the future (UTC)."
            )
        return value

    def create(self, validated_data):
        """
        Create notification with status 'scheduled' and associate with authenticated user.
        """
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'scheduled'
        return super().create(validated_data)


class NotificationRetrySerializer(serializers.Serializer):
    """
    Empty serializer used for retry endpoint.
    No input fields required.
    """
    pass