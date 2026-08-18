from django.db import models
from profiles.models import StudentProfile
from opportunities.models import Opportunity

class Match(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='opportunity_matches')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='student_matches')
    match_score_pct = models.IntegerField(default=0)
    skill_coverage_score = models.FloatField(default=0.0)
    evidence_strength_score = models.FloatField(default=0.0)
    project_relevance_score = models.FloatField(default=0.0)
    experience_score = models.FloatField(default=0.0)
    credential_score = models.FloatField(default=0.0)
    explanation_json = models.JSONField(default=dict)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'opportunity')
        ordering = ['-match_score_pct']

    def __str__(self):
        return f"{self.student.user.username} <-> {self.opportunity.title}: {self.match_score_pct}%"
