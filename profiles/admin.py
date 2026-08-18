from django.contrib import admin
from .models import University, StudentProfile, RecruiterProfile

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'verified')
    search_fields = ('name', 'location')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'passport_slug', 'university', 'degree', 'overall_skill_score')
    search_fields = ('user__username', 'user__first_name', 'passport_slug', 'university')

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'designation', 'verified')
    search_fields = ('company_name', 'user__username')
