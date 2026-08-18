from django.urls import path
from . import views

urlpatterns = [
    path('api/data/', views.student_analytics_data, name='analytics_data'),
]
