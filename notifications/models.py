from django.db import models
from django.conf import settings

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        VERIFICATION = 'VERIFICATION', 'Verification Status'
        MATCH = 'MATCH', 'Opportunity Match'
        SKILL_GAP = 'SKILL_GAP', 'Skill Gap Alert'
        TEAM_INVITE = 'TEAM_INVITE', 'Team Invitation'
        SYSTEM = 'SYSTEM', 'System Alert'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.MATCH)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link_url = models.CharField(max_length=255, blank=True, default='/dashboard/')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
