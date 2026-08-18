from django.db import models

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default='fa-solid fa-code', help_text="FontAwesome icon class")

    def __str__(self):
        return f"{self.name} ({self.category.name})"
