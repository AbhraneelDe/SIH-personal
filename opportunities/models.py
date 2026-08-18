from django.db import models
from profiles.models import RecruiterProfile, StudentProfile
from skills.models import Skill

class Opportunity(models.Model):
    class Category(models.TextChoices):
        INTERNSHIP = 'INTERNSHIP', 'Internship'
        JOB = 'JOB', 'Full-Time Job'
        RESEARCH = 'RESEARCH', 'Research Opportunity'
        HACKATHON = 'HACKATHON', 'Hackathon'
        COMPETITION = 'COMPETITION', 'Competition'
        FREELANCE = 'FREELANCE', 'Freelance / Industry Project'
        CAMPUS_PROJECT = 'CAMPUS_PROJECT', 'Campus Project'
        TEAM_OPPORTUNITY = 'TEAM_OPPORTUNITY', 'Team Opportunity'

    class LocationType(models.TextChoices):
        REMOTE = 'REMOTE', 'Remote'
        HYBRID = 'HYBRID', 'Hybrid'
        ON_SITE = 'ON_SITE', 'On-Site'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', 'Entry-Level / Student'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        ADVANCED = 'ADVANCED', 'Advanced'

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.INTERNSHIP)
    description = models.TextField()
    location = models.CharField(max_length=150, default="San Francisco, CA / Remote")
    location_type = models.CharField(max_length=20, choices=LocationType.choices, default=LocationType.HYBRID)
    duration = models.CharField(max_length=100, default="3 - 6 Months")
    stipend = models.CharField(max_length=100, default="$3,500 - $5,000 / month")
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.organization}"

class OpportunitySkill(models.Model):
    class SkillRequirementType(models.TextChoices):
        REQUIRED = 'REQUIRED', 'Required Skill'
        PREFERRED = 'PREFERRED', 'Preferred Skill'

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='opportunity_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='opportunity_requirements')
    requirement_type = models.CharField(max_length=20, choices=SkillRequirementType.choices, default=SkillRequirementType.REQUIRED)
    min_proficiency_score = models.IntegerField(default=70, help_text="Minimum score 0-100 expected")

    def __str__(self):
        return f"{self.opportunity.title} -> {self.skill.name} ({self.requirement_type})"

class SavedOpportunity(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='saved_opportunities')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='saved_by_students')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'opportunity')
