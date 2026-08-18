from django.db import models
from profiles.models import StudentProfile
from skills.models import SkillCategory, Skill

class Team(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Smart Campus AI Project")
    description = models.TextField(help_text="Project scope and goal")
    leader = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='led_teams')
    required_skill_categories = models.ManyToManyField(SkillCategory, related_name='teams_requiring_category')
    required_skills = models.ManyToManyField(Skill, related_name='teams_requiring_skill', blank=True)
    max_members = models.IntegerField(default=4)
    complementarity_score = models.IntegerField(default=92)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Led by {self.leader.user.username})"

class TeamMember(models.Model):
    class RoleInTeam(models.TextChoices):
        LEADER = 'LEADER', 'Team Lead'
        BACKEND = 'BACKEND', 'Backend Engineer'
        FRONTEND = 'FRONTEND', 'Frontend / UI Specialist'
        ML_AI = 'ML_AI', 'AI / ML Specialist'
        CLOUD = 'CLOUD', 'Cloud / DevOps Specialist'
        BUSINESS = 'BUSINESS', 'Product & Business Analyst'

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=30, choices=RoleInTeam.choices, default=RoleInTeam.BACKEND)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'student')

    def __str__(self):
        return f"{self.student.user.username} in {self.team.title} ({self.get_role_display()})"
