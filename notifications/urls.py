from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:pk>/retry/', views.NotificationRetryView.as_view(), name='notification-retry'),
]