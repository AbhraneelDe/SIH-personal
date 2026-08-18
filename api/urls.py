from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentProfileViewSet, SkillViewSet, EvidenceViewSet,
    OpportunityViewSet, TeamViewSet, ApplicationViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'evidence', EvidenceViewSet, basename='evidence')
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
