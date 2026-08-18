from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'match_score_pct', 'calculated_at')
    list_filter = ('match_score_pct',)
    search_fields = ('student__user__username', 'opportunity__title')
