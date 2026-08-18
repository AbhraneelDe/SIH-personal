from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.models import StudentProfile
from opportunities.models import Opportunity
from .services import ExplainableMatchingEngine

@login_required
def skill_gaps_view(request):
    try:
        student = request.user.student_profile
    except AttributeError:
        student = StudentProfile.objects.first()

    opportunities = Opportunity.objects.filter(is_active=True)[:10]

    all_missing = []
    for opp in opportunities:
        explanation = ExplainableMatchingEngine.calculate_match(student, opp)
        for ms in explanation['missing_skills']:
            all_missing.append({
                'skill_name': ms['skill_name'],
                'target_opportunity': opp.title,
                'requirement_type': ms['requirement_type'],
                'current_score': ms['current_score'],
                'target_score': ms['target_score'],
                'priority': 'High' if ms['requirement_type'] == 'Required Skill' else 'Medium',
                'action': f"Complete a hands-on project or verified course in {ms['skill_name']}."
            })

    unique_gaps = {}
    for item in all_missing:
        name = item['skill_name']
        if name not in unique_gaps:
            unique_gaps[name] = item

    context = {
        'student': student,
        'skill_gaps': list(unique_gaps.values()),
    }
    return render(request, 'skills/gap_analysis.html', context)
