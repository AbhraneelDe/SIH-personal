from django.db import models
from profiles.models import StudentProfile
from opportunities.models import Opportunity

class Application(models.Model):
    class ApplicationStatus(models.TextChoices):
        APPLIED = 'APPLIED', 'Application Submitted'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Evidence Review'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Not Selected'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    cover_note = models.TextField(blank=True, help_text="Brief statement linking verified projects to role")
    status = models.CharField(max_length=25, choices=ApplicationStatus.choices, default=ApplicationStatus.APPLIED)
    match_score_pct_at_apply = models.IntegerField(default=0)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'opportunity')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.user.username} -> {self.opportunity.title} [{self.get_status_display()}]"
