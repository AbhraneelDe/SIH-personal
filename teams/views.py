from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.models import StudentProfile
from .models import Team, TeamMember
from .services import TeamMatchingEngine

@login_required
def teams_view(request):
    try:
        leader = request.user.student_profile
    except AttributeError:
        leader = StudentProfile.objects.first()

    my_teams = Team.objects.filter(leader=leader)
    recommendations = TeamMatchingEngine.get_complementary_teammates(leader)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            team = Team.objects.create(
                title=title,
                description=description or "Multidisciplinary innovation team project.",
                leader=leader,
                complementarity_score=94
            )
            TeamMember.objects.create(
                team=team,
                student=leader,
                role=TeamMember.RoleInTeam.LEADER
            )
            messages.success(request, f"Project team '{team.title}' created successfully!")
            return redirect('teams_view')

    context = {
        'leader': leader,
        'my_teams': my_teams,
        'recommended_teammates': recommendations,
    }
    return render(request, 'teams/matching.html', context)
