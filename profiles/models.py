from django.db import models
from django.conf import settings

class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    university = models.CharField(max_length=200, default="Stanford University")
    degree = models.CharField(max_length=200, default="B.Tech Computer Science")
    graduation_year = models.IntegerField(default=2026)
    summary = models.TextField(
        blank=True,
        default="Passionate computer science student specializing in AI/ML, backend microservices, and full-stack development. Focused on building evidence-backed engineering projects."
    )
    overall_skill_score = models.IntegerField(default=88, help_text="Overall evidence-backed score 0-100")
    passport_slug = models.SlugField(max_length=100, unique=True)
    github_url = models.URLField(blank=True, default="https://github.com/alexmorgan")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/in/alexmorgan")
    portfolio_url = models.URLField(blank=True, default="https://alexmorgan.dev")
    avatar_url = models.URLField(blank=True, default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80")
    profile_completion_pct = models.IntegerField(default=85)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.passport_slug})"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recruiter_profile'
    )
    company_name = models.CharField(max_length=200, default="TechCorp Global")
    industry = models.CharField(max_length=100, default="Artificial Intelligence & Software")
    designation = models.CharField(max_length=150, default="Lead Talent Specialist")
    website = models.URLField(blank=True, default="https://techcorp.example.com")
    company_logo_url = models.URLField(blank=True, default="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&auto=format&fit=crop&q=80")
    verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company_name}"
