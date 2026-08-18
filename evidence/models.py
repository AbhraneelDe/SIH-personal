from django.db import models
from profiles.models import StudentProfile
from skills.models import Skill

class Evidence(models.Model):
    class EvidenceType(models.TextChoices):
        COURSEWORK = 'COURSEWORK', 'Verified Coursework'
        PROJECT = 'PROJECT', 'Practical Project'
        COMPETITION = 'COMPETITION', 'Hackathon / Competition'
        CREDENTIAL = 'CREDENTIAL', 'Micro-Credential / Certificate'
        GITHUB = 'GITHUB', 'GitHub Repository'
        EXPERIENCE = 'EXPERIENCE', 'Internship / Practical Experience'

    class VerificationStatus(models.TextChoices):
        VERIFIED = 'VERIFIED', 'Verified'
        PENDING = 'PENDING', 'Pending Verification'
        REJECTED = 'REJECTED', 'Rejected'
        EXPIRED = 'EXPIRED', 'Expired'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='evidence_items')
    evidence_type = models.CharField(max_length=30, choices=EvidenceType.choices, default=EvidenceType.PROJECT)
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200, help_text="e.g. Stanford University, Google, Coursera, Major League Hacking")
    issue_date = models.DateField()
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.VERIFIED)
    url_or_link = models.URLField(blank=True, help_text="Certificate URL, GitHub repository link, or proof link")
    description = models.TextField(blank=True)
    confidence_level = models.IntegerField(default=90, help_text="Evidence confidence rating percentage 0-100")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} ({self.get_evidence_type_display()}) - {self.student.user.username}"

class SkillEvidence(models.Model):
    class ProficiencyLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', 'Beginner'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        ADVANCED = 'ADVANCED', 'Advanced'
        EXPERT = 'EXPERT', 'Expert'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skill_evidences')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_evidences')
    proficiency = models.CharField(max_length=20, choices=ProficiencyLevel.choices, default=ProficiencyLevel.ADVANCED)
    score_pct = models.IntegerField(default=85, help_text="Evidence strength score percentage 0-100")
    evidences = models.ManyToManyField(Evidence, related_name='linked_skills', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'skill')
        ordering = ['-score_pct']

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name}: {self.score_pct}% ({self.proficiency})"

class EvidenceVerification(models.Model):
    evidence = models.OneToOneField(Evidence, on_delete=models.CASCADE, related_name='verification_record')
    verified_by = models.CharField(max_length=150, default="Automated Verification System")
    verification_notes = models.TextField(blank=True, default="Verified via institutional API signature & GitHub repository commit hash check.")
    verified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.evidence.title}"
