from django.urls import path
from . import views

urlpatterns = [
    path('mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
]
