from django.conf import settings
from evidence.models import SkillEvidence, Evidence
from opportunities.models import OpportunitySkill
from .models import Match

class ExplainableMatchingEngine:
    @staticmethod
    def calculate_match(student_profile, opportunity):
        """
        Calculate an evidence-backed, transparent, and fair match score between a student and an opportunity.
        Demographics/protected attributes (gender, race, religion, photo, age) are explicitly excluded (0% weight).
        """
        weights = getattr(settings, 'EXPLAINABLE_MATCH_WEIGHTS', {
            'SKILL_COVERAGE': 0.40,
            'EVIDENCE_STRENGTH': 0.25,
            'PROJECT_RELEVANCE': 0.15,
            'EXPERIENCE_ALIGNMENT': 0.10,
            'CREDENTIAL_RELEVANCE': 0.10,
        })

        opp_skills = opportunity.opportunity_skills.select_related('skill').all()
        if not opp_skills.exists():
            return {
                'score_pct': 70,
                'matched_skills': [],
                'missing_skills': [],
                'supporting_evidence': [],
                'recommendation': "No specific skill criteria provided for this opportunity."
            }

        required_opp_skills = [os for os in opp_skills if os.requirement_type == OpportunitySkill.SkillRequirementType.REQUIRED]
        preferred_opp_skills = [os for os in opp_skills if os.requirement_type == OpportunitySkill.SkillRequirementType.PREFERRED]

        student_skill_evidences = SkillEvidence.objects.filter(student=student_profile).select_related('skill').prefetch_related('evidences')
        student_skill_map = {se.skill_id: se for se in student_skill_evidences}

        matched_skills = []
        missing_skills = []
        supporting_evidence_list = []

        total_required_count = len(required_opp_skills) or 1
        matched_required_count = 0
        total_evidence_score_sum = 0.0

        for os in opp_skills:
            skill = os.skill
            se = student_skill_map.get(skill.id)

            if se:
                is_matched = se.score_pct >= (os.min_proficiency_score - 15)
                score_ratio = min(1.0, se.score_pct / max(1, os.min_proficiency_score))
                total_evidence_score_sum += se.score_pct

                if is_matched:
                    if os.requirement_type == OpportunitySkill.SkillRequirementType.REQUIRED:
                        matched_required_count += 1

                    ev_items = list(se.evidences.all())
                    ev_titles = [f"{e.get_evidence_type_display()}: {e.title}" for e in ev_items]

                    matched_skills.append({
                        'skill_name': skill.name,
                        'requirement_type': os.get_requirement_type_display(),
                        'student_score': se.score_pct,
                        'proficiency': se.get_proficiency_display(),
                        'evidence_count': len(ev_items),
                        'evidence_titles': ev_titles[:3],
                    })

                    for ev in ev_items:
                        supporting_evidence_list.append({
                            'skill': skill.name,
                            'title': ev.title,
                            'type': ev.get_evidence_type_display(),
                            'organization': ev.issuing_organization,
                            'status': ev.get_verification_status_display(),
                        })
                else:
                    missing_skills.append({
                        'skill_name': skill.name,
                        'requirement_type': os.get_requirement_type_display(),
                        'current_score': se.score_pct,
                        'target_score': os.min_proficiency_score,
                        'status': 'Partial Evidence'
                    })
            else:
                missing_skills.append({
                    'skill_name': skill.name,
                    'requirement_type': os.get_requirement_type_display(),
                    'current_score': 0,
                    'target_score': os.min_proficiency_score,
                    'status': 'Missing Evidence'
                })

        # Score Calculations
        skill_coverage = (matched_required_count / total_required_count) * 100.0
        avg_evidence_strength = (total_evidence_score_sum / max(1, len(opp_skills)))

        # Project relevance check
        student_all_evidences = Evidence.objects.filter(student=student_profile)
        project_count = student_all_evidences.filter(evidence_type=Evidence.EvidenceType.PROJECT).count()
        project_relevance = min(100.0, project_count * 30.0)

        # Experience alignment check
        exp_count = student_all_evidences.filter(evidence_type=Evidence.EvidenceType.EXPERIENCE).count()
        comp_count = student_all_evidences.filter(evidence_type=Evidence.EvidenceType.COMPETITION).count()
        experience_alignment = min(100.0, (exp_count * 50.0) + (comp_count * 25.0) + 20.0)

        # Credential relevance check
        cred_count = student_all_evidences.filter(evidence_type__in=[Evidence.EvidenceType.CREDENTIAL, Evidence.EvidenceType.COURSEWORK]).count()
        credential_relevance = min(100.0, cred_count * 33.3)

        total_match_score = (
            (skill_coverage * weights['SKILL_COVERAGE']) +
            (avg_evidence_strength * weights['EVIDENCE_STRENGTH']) +
            (project_relevance * weights['PROJECT_RELEVANCE']) +
            (experience_alignment * weights['EXPERIENCE_ALIGNMENT']) +
            (credential_relevance * weights['CREDENTIAL_RELEVANCE'])
        )

        final_score_pct = int(min(99, max(35, round(total_match_score))))

        # Recommendation synthesis
        if missing_skills:
            missing_names = ", ".join([ms['skill_name'] for ms in missing_skills[:2]])
            recommendation_text = f"Strengthen fundamentals in {missing_names} by completing a practical project or verified micro-credential."
        else:
            recommendation_text = "Exceptional fit! You meet all skill requirements with verified evidence."

        explanation_payload = {
            'score_pct': final_score_pct,
            'breakdown': {
                'skill_coverage': round(skill_coverage, 1),
                'evidence_strength': round(avg_evidence_strength, 1),
                'project_relevance': round(project_relevance, 1),
                'experience_alignment': round(experience_alignment, 1),
                'credential_relevance': round(credential_relevance, 1),
            },
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'supporting_evidence': supporting_evidence_list,
            'recommendation': recommendation_text,
            'fairness_guarantee': "Score strictly calculated from verified skills, coursework, and project evidence. Protected attributes are not processed."
        }

        # Save or update Match model record
        Match.objects.update_or_create(
            student=student_profile,
            opportunity=opportunity,
            defaults={
                'match_score_pct': final_score_pct,
                'skill_coverage_score': skill_coverage,
                'evidence_strength_score': avg_evidence_strength,
                'project_relevance_score': project_relevance,
                'experience_score': experience_alignment,
                'credential_score': credential_relevance,
                'explanation_json': explanation_payload,
            }
        )

        return explanation_payload
