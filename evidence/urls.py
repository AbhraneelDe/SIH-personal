from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_evidence, name='manage_evidence'),
]
