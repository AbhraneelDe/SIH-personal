from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.models import StudentProfile
from .models import Application

@login_required
def applications_list(request):
    try:
        student = request.user.student_profile
    except AttributeError:
        student = StudentProfile.objects.first()

    apps = Application.objects.filter(student=student).select_related('opportunity') if student else Application.objects.none()

    return render(request, 'applications/list.html', {
        'student': student,
        'applications': apps,
    })
