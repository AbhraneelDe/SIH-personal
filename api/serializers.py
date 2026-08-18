from rest_framework import serializers
from accounts.models import User
from profiles.models import StudentProfile, RecruiterProfile
from skills.models import SkillCategory, Skill
from evidence.models import Evidence, SkillEvidence
from opportunities.models import Opportunity, OpportunitySkill
from matching.models import Match
from teams.models import Team
from applications.models import Application
from notifications.models import Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'

class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    category = SkillCategorySerializer(read_only=True)

    class Meta:
        model = Skill
        fields = '__all__'

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = '__all__'

class SkillEvidenceSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    evidences = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = SkillEvidence
        fields = '__all__'

class OpportunitySkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = OpportunitySkill
        fields = '__all__'

class OpportunitySerializer(serializers.ModelSerializer):
    opportunity_skills = OpportunitySkillSerializer(many=True, read_only=True)

    class Meta:
        model = Opportunity
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    opportunity = OpportunitySerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    leader = StudentProfileSerializer(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    opportunity = OpportunitySerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
