from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'status', 'match_score_pct_at_apply', 'applied_at')
    list_filter = ('status',)
    search_fields = ('student__user__username', 'opportunity__title')
