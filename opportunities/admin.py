from django.contrib import admin
from .models import Opportunity, OpportunitySkill, SavedOpportunity

class OpportunitySkillInline(admin.TabularInline):
    model = OpportunitySkill
    extra = 2

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'category', 'location_type', 'is_active', 'application_deadline')
    list_filter = ('category', 'location_type', 'is_active')
    search_fields = ('title', 'organization', 'description')
    inlines = [OpportunitySkillInline]

@admin.register(OpportunitySkill)
class OpportunitySkillAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'skill', 'requirement_type', 'min_proficiency_score')
    list_filter = ('requirement_type', 'skill')

@admin.register(SavedOpportunity)
class SavedOpportunityAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'created_at')
