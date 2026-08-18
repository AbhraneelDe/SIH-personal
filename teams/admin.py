from django.contrib import admin
from .models import Team, TeamMember

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title', 'leader', 'max_members', 'complementarity_score', 'created_at')
    search_fields = ('title', 'description', 'leader__user__username')
    inlines = [TeamMemberInline]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'student', 'role', 'joined_at')
    list_filter = ('role',)
