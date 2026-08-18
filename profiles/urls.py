from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_overview, name='dashboard_overview'),
    path('passport/<slug:slug>/', views.public_passport, name='public_passport'),
    path('passport/<slug:slug>/print/', views.export_passport_print, name='export_passport_print'),
]
