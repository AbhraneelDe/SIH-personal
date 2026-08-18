from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from opportunities.models import Opportunity, OpportunitySkill
from applications.models import Application
from profiles.models import StudentProfile, RecruiterProfile
from skills.models import Skill
from matching.services import ExplainableMatchingEngine

@login_required
def recruiter_dashboard(request):
    try:
        recruiter = request.user.recruiter_profile
    except AttributeError:
        # Fallback or redirect if not recruiter
        recruiter = RecruiterProfile.objects.first()

    opportunities = Opportunity.objects.filter(recruiter=recruiter) if recruiter else Opportunity.objects.all()[:5]
    applications = Application.objects.filter(opportunity__in=opportunities).select_related('student__user', 'opportunity')

    context = {
        'recruiter': recruiter,
        'opportunities': opportunities,
        'applications': applications,
        'total_opportunities': opportunities.count() if hasattr(opportunities, 'count') else len(opportunities),
        'total_applicants': len(applications),
        'shortlisted_count': sum(1 for a in applications if a.status == Application.ApplicationStatus.SHORTLISTED)
    }
    return render(request, 'recruiter/dashboard.html', context)

@login_required
def create_opportunity_view(request):
    skills = Skill.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        organization = request.POST.get('organization')
        category = request.POST.get('category', Opportunity.Category.INTERNSHIP)
        description = request.POST.get('description')
        location = request.POST.get('location')
        location_type = request.POST.get('location_type', Opportunity.LocationType.HYBRID)
        duration = request.POST.get('duration')
        stipend = request.POST.get('stipend')
        deadline = request.POST.get('application_deadline')
        selected_skills = request.POST.getlist('skills')

        recruiter_prof = getattr(request.user, 'recruiter_profile', None)

        opp = Opportunity.objects.create(
            recruiter=recruiter_prof,
            title=title,
            organization=organization or (recruiter_prof.company_name if recruiter_prof else "Tech Organization"),
            category=category,
            description=description,
            location=location or "Remote",
            location_type=location_type,
            duration=duration or "3 Months",
            stipend=stipend or "$4,000 / month",
            application_deadline=deadline or "2026-12-31"
        )

        for skill_id in selected_skills:
            skill = Skill.objects.get(id=skill_id)
            OpportunitySkill.objects.create(
                opportunity=opp,
                skill=skill,
                requirement_type=OpportunitySkill.SkillRequirementType.REQUIRED,
                min_proficiency_score=75
            )

        messages.success(request, f"Opportunity '{opp.title}' published successfully!")
        return redirect('recruiter_dashboard')

    return render(request, 'recruiter/create_opportunity.html', {'skills': skills})

@login_required
def candidate_search(request):
    query = request.GET.get('q', '')
    students = StudentProfile.objects.all().select_related('user')
    if query:
        students = students.filter(
            user__first_name__icontains=query
        ) | students.filter(
            degree__icontains=query
        ) | students.filter(
            summary__icontains=query
        )
    return render(request, 'recruiter/candidate_search.html', {'students': students, 'query': query})

@login_required
def applicant_detail(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    explanation = ExplainableMatchingEngine.calculate_match(app.student, app.opportunity)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.ApplicationStatus.choices):
            app.status = new_status
            app.save()
            messages.success(request, f"Application status updated to {app.get_status_display()}")
            return redirect('applicant_detail', app_id=app.id)

    context = {
        'application': app,
        'student': app.student,
        'opportunity': app.opportunity,
        'match_explanation': explanation,
    }
    return render(request, 'recruiter/applicant_detail.html', context)
