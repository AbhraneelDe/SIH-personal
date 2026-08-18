from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Opportunity
from applications.models import Application
from profiles.models import StudentProfile
from matching.services import ExplainableMatchingEngine

def opportunities_list(request):
    category = request.GET.get('category', '')
    location_type = request.GET.get('location_type', '')
    query = request.GET.get('q', '')

    opportunities = Opportunity.objects.filter(is_active=True)

    if category:
        opportunities = opportunities.filter(category=category)
    if location_type:
        opportunities = opportunities.filter(location_type=location_type)
    if query:
        opportunities = opportunities.filter(title__icontains=query) | opportunities.filter(description__icontains=query)

    student = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
    else:
        student = StudentProfile.objects.first()

    matched_opps = []
    for opp in opportunities:
        match_info = ExplainableMatchingEngine.calculate_match(student, opp) if student else {'score_pct': 75}
        matched_opps.append({
            'opp': opp,
            'match_score': match_info['score_pct']
        })

    matched_opps.sort(key=lambda x: x['match_score'], reverse=True)

    context = {
        'opportunities': matched_opps,
        'categories': Opportunity.Category.choices,
        'location_types': Opportunity.LocationType.choices,
        'selected_category': category,
        'selected_location': location_type,
        'query': query,
    }
    return render(request, 'opportunities/index.html', context)

def opportunity_detail(request, opp_id):
    opp = get_object_or_404(Opportunity, id=opp_id)

    student = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
    else:
        student = StudentProfile.objects.first()

    match_explanation = ExplainableMatchingEngine.calculate_match(student, opp) if student else None

    already_applied = False
    if request.user.is_authenticated and student:
        already_applied = Application.objects.filter(student=student, opportunity=opp).exists()

    context = {
        'opportunity': opp,
        'match_explanation': match_explanation,
        'already_applied': already_applied,
        'student': student
    }
    return render(request, 'opportunities/detail.html', context)

@login_required
def apply_opportunity(request, opp_id):
    opp = get_object_or_404(Opportunity, id=opp_id)
    try:
        student = request.user.student_profile
    except AttributeError:
        messages.error(request, "Only student profiles can apply for opportunities.")
        return redirect('opportunity_detail', opp_id=opp.id)

    if request.method == 'POST':
        cover_note = request.POST.get('cover_note', '')
        explanation = ExplainableMatchingEngine.calculate_match(student, opp)

        Application.objects.get_or_create(
            student=student,
            opportunity=opp,
            defaults={
                'cover_note': cover_note,
                'match_score_pct_at_apply': explanation['score_pct'],
                'status': Application.ApplicationStatus.APPLIED
            }
        )

        messages.success(request, f"Application for '{opp.title}' submitted successfully!")
        return redirect('applications_list')

    return redirect('opportunity_detail', opp_id=opp.id)
