from django.test import TestCase
from accounts.models import User
from profiles.models import StudentProfile
from skills.models import SkillCategory, Skill
from evidence.models import Evidence, SkillEvidence
from opportunities.models import Opportunity, OpportunitySkill
from matching.services import ExplainableMatchingEngine

class ExplainableMatchingEngineTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_student', role=User.Role.STUDENT)
        self.profile = StudentProfile.objects.create(user=self.user, passport_slug='test_student')

        cat = SkillCategory.objects.create(name='Backend')
        self.python_skill = Skill.objects.create(name='Python', category=cat)
        self.docker_skill = Skill.objects.create(name='Docker', category=cat)

        self.ev = Evidence.objects.create(
            student=self.profile,
            evidence_type=Evidence.EvidenceType.COURSEWORK,
            title='Python Fundamentals',
            issuing_organization='Test Uni',
            issue_date='2026-01-01',
            verification_status=Evidence.VerificationStatus.VERIFIED
        )

        self.se = SkillEvidence.objects.create(
            student=self.profile,
            skill=self.python_skill,
            score_pct=90
        )
        self.se.evidences.add(self.ev)

        self.opp = Opportunity.objects.create(
            title='Backend Intern',
            organization='TestCorp',
            description='Test role',
            application_deadline='2026-12-31'
        )

        OpportunitySkill.objects.create(
            opportunity=self.opp,
            skill=self.python_skill,
            requirement_type=OpportunitySkill.SkillRequirementType.REQUIRED,
            min_proficiency_score=75
        )
        OpportunitySkill.objects.create(
            opportunity=self.opp,
            skill=self.docker_skill,
            requirement_type=OpportunitySkill.SkillRequirementType.REQUIRED,
            min_proficiency_score=70
        )

    def test_explainable_match_calculation(self):
        explanation = ExplainableMatchingEngine.calculate_match(self.profile, self.opp)
        self.assertIn('score_pct', explanation)
        self.assertTrue(35 <= explanation['score_pct'] <= 99)

        # Check matched vs missing skills
        matched_names = [m['skill_name'] for m in explanation['matched_skills']]
        missing_names = [m['skill_name'] for m in explanation['missing_skills']]

        self.assertIn('Python', matched_names)
        self.assertIn('Docker', missing_names)
        self.assertIn('fairness_guarantee', explanation)
