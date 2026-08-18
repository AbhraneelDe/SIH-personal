from django.contrib import admin
from .models import Evidence, SkillEvidence, EvidenceVerification

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'evidence_type', 'verification_status', 'issue_date')
    list_filter = ('evidence_type', 'verification_status')
    search_fields = ('title', 'issuing_organization', 'student__user__username')

@admin.register(SkillEvidence)
class SkillEvidenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'proficiency', 'score_pct')
    list_filter = ('proficiency', 'skill')
    search_fields = ('student__user__username', 'skill__name')

@admin.register(EvidenceVerification)
class EvidenceVerificationAdmin(admin.ModelAdmin):
    list_display = ('evidence', 'verified_by', 'verified_at')
