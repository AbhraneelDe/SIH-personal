from django.urls import path
from . import views

urlpatterns = [
    path('', views.applications_list, name='applications_list'),
]
