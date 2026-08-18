from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from profiles.models import StudentProfile
from evidence.models import Evidence, SkillEvidence
from opportunities.models import Opportunity
from matching.models import Match

@login_required
def student_analytics_data(request):
    try:
        student = request.user.student_profile
    except AttributeError:
        # Fallback to demo profile Alex Morgan if superuser or recruiter viewing analytics
        student = StudentProfile.objects.first()

    if not student:
        return JsonResponse({'error': 'No profile'}, status=404)

    # 1. Skill Scores
    skill_evs = SkillEvidence.objects.filter(student=student).select_related('skill')
    skill_labels = [se.skill.name for se in skill_evs]
    skill_scores = [se.score_pct for se in skill_evs]

    # 2. Verified Evidence by Category
    ev_items = Evidence.objects.filter(student=student)
    cat_counts = {}
    for ev in ev_items:
        t = ev.get_evidence_type_display()
        cat_counts[t] = cat_counts.get(t, 0) + 1

    # 3. Matches
    matches = Match.objects.filter(student=student).select_related('opportunity')[:6]
    match_labels = [m.opportunity.title[:18] + '...' for m in matches]
    match_scores = [m.match_score_pct for m in matches]

    return JsonResponse({
        'skills': {
            'labels': skill_labels,
            'data': skill_scores,
        },
        'evidence_categories': {
            'labels': list(cat_counts.keys()),
            'data': list(cat_counts.values()),
        },
        'matches': {
            'labels': match_labels,
            'data': match_scores,
        },
        'overall_score': student.overall_skill_score,
        'profile_completion': student.profile_completion_pct
    })
