from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from profiles.models import StudentProfile
from skills.models import Skill, SkillCategory
from evidence.models import Evidence, SkillEvidence
from opportunities.models import Opportunity
from matching.models import Match
from matching.services import ExplainableMatchingEngine
from teams.models import Team
from teams.services import TeamMatchingEngine
from applications.models import Application
from notifications.models import Notification

from .serializers import (
    StudentProfileSerializer, SkillSerializer, SkillCategorySerializer,
    EvidenceSerializer, SkillEvidenceSerializer, OpportunitySerializer,
    MatchSerializer, TeamSerializer, ApplicationSerializer, NotificationSerializer
)

class StudentProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    lookup_field = 'passport_slug'

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            return Evidence.objects.filter(student=self.request.user.student_profile)
        return Evidence.objects.none()

class OpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Opportunity.objects.filter(is_active=True)
    serializer_class = OpportunitySerializer

    @action(detail=True, methods=['get'])
    def explain_match(self, request, pk=None):
        opportunity = self.get_object()
        if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
        else:
            student = StudentProfile.objects.first()

        explanation = ExplainableMatchingEngine.calculate_match(student, opportunity)
        return Response(explanation)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=False, methods=['get'])
    def recommend_members(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
            leader = request.user.student_profile
        else:
            leader = StudentProfile.objects.first()

        recommendations = TeamMatchingEngine.get_complementary_teammates(leader)
        return Response(recommendations)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            return Application.objects.filter(student=self.request.user.student_profile)
        return Application.objects.none()

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Notification.objects.filter(user=self.request.user)
        return Notification.objects.none()
