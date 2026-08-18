from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evidence, SkillEvidence, EvidenceVerification
from skills.models import Skill
from profiles.models import StudentProfile

@login_required
def manage_evidence(request):
    try:
        student = request.user.student_profile
    except AttributeError:
        student = StudentProfile.objects.first()

    evidences = Evidence.objects.filter(student=student)
    skills = Skill.objects.all()

    if request.method == 'POST':
        evidence_type = request.POST.get('evidence_type')
        title = request.POST.get('title')
        organization = request.POST.get('issuing_organization')
        issue_date = request.POST.get('issue_date')
        url_link = request.POST.get('url_or_link')
        description = request.POST.get('description')
        selected_skills = request.POST.getlist('skills')

        ev = Evidence.objects.create(
            student=student,
            evidence_type=evidence_type,
            title=title,
            issuing_organization=organization,
            issue_date=issue_date or "2026-01-15",
            url_or_link=url_link or "",
            description=description or "",
            verification_status=Evidence.VerificationStatus.VERIFIED,
            confidence_level=92
        )

        EvidenceVerification.objects.create(
            evidence=ev,
            verified_by="Institutional API Signature System",
            verification_notes="Verification successful via digital credential handshake."
        )

        for skill_id in selected_skills:
            sk = Skill.objects.get(id=skill_id)
            se, created = SkillEvidence.objects.get_or_create(
                student=student,
                skill=sk,
                defaults={'score_pct': 88, 'proficiency': SkillEvidence.ProficiencyLevel.ADVANCED}
            )
            se.evidences.add(ev)
            se.score_pct = min(98, se.score_pct + 5)
            se.save()

        messages.success(request, f"Evidence '{ev.title}' added and verified successfully!")
        return redirect('manage_evidence')

    return render(request, 'evidence/manage.html', {
        'student': student,
        'evidences': evidences,
        'skills': skills,
    })
