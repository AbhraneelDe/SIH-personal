from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('opportunity/create/', views.create_opportunity_view, name='create_opportunity'),
    path('candidates/', views.candidate_search, name='candidate_search'),
    path('applicant/<int:app_id>/', views.applicant_detail, name='applicant_detail'),
]
