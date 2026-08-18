from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from evidence.models import Evidence, SkillEvidence
from opportunities.models import Opportunity
from matching.models import Match
from matching.services import ExplainableMatchingEngine

def home_view(request):
    featured_opportunities = Opportunity.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {
        'featured_opportunities': featured_opportunities,
    })

@login_required
def dashboard_overview(request):
    if request.user.is_recruiter:
        return redirect('recruiter_dashboard')

    try:
        student = request.user.student_profile
    except AttributeError:
        student = StudentProfile.objects.first()

    evidences = Evidence.objects.filter(student=student)
    skill_evidences = SkillEvidence.objects.filter(student=student).select_related('skill')

    opportunities = Opportunity.objects.filter(is_active=True)
    matches = []
    for opp in opportunities[:8]:
        explanation = ExplainableMatchingEngine.calculate_match(student, opp)
        matches.append({
            'opportunity': opp,
            'match': explanation
        })

    matches.sort(key=lambda x: x['match']['score_pct'], reverse=True)

    # Calculate skill gap summary
    all_missing_skills = []
    for m in matches[:4]:
        all_missing_skills.extend(m['match']['missing_skills'])

    unique_gaps = {ms['skill_name']: ms for ms in all_missing_skills}.values()

    context = {
        'student': student,
        'evidence_count': evidences.count(),
        'verified_count': evidences.filter(verification_status=Evidence.VerificationStatus.VERIFIED).count(),
        'opportunity_matches_count': len(matches),
        'top_matches': matches[:5],
        'skill_gaps': list(unique_gaps)[:4],
        'skill_evidences': skill_evidences,
    }
    return render(request, 'dashboard/overview.html', context)

def public_passport(request, slug):
    student = get_object_or_404(StudentProfile, passport_slug=slug)
    evidences = Evidence.objects.filter(student=student)
    skill_evidences = SkillEvidence.objects.filter(student=student).select_related('skill').prefetch_related('evidences')

    context = {
        'student': student,
        'evidences': evidences,
        'skill_evidences': skill_evidences,
        'verified_count': evidences.filter(verification_status=Evidence.VerificationStatus.VERIFIED).count(),
        'is_owner': request.user.is_authenticated and hasattr(request.user, 'student_profile') and request.user.student_profile == student
    }
    return render(request, 'passport/view.html', context)

def export_passport_print(request, slug):
    student = get_object_or_404(StudentProfile, passport_slug=slug)
    evidences = Evidence.objects.filter(student=student)
    skill_evidences = SkillEvidence.objects.filter(student=student).select_related('skill')

    return render(request, 'passport/print_pdf.html', {
        'student': student,
        'evidences': evidences,
        'skill_evidences': skill_evidences,
    })
