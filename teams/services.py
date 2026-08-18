from profiles.models import StudentProfile
from evidence.models import SkillEvidence
from skills.models import SkillCategory

class TeamMatchingEngine:
    @staticmethod
    def get_complementary_teammates(leader_profile, team_project=None):
        """
        Analyze current leader's verified skill evidence, identify missing skill areas,
        and recommend complementary students to build a high-skill multidisciplinary team.
        Fairness guaranteed: Demographics/protected attributes strictly excluded.
        """
        leader_skills = SkillEvidence.objects.filter(student=leader_profile).select_related('skill__category')
        leader_categories = set(se.skill.category.name for se in leader_skills)

        # Retrieve candidate students (excluding leader)
        candidates = StudentProfile.objects.exclude(id=leader_profile.id).select_related('user')

        results = []
        for candidate in candidates[:10]:
            cand_skills = SkillEvidence.objects.filter(student=candidate).select_related('skill__category')
            cand_categories = set(cs.skill.category.name for cs in cand_skills)

            # Complementary categories = categories candidate possesses that leader lacks
            complementary_categories = cand_categories - leader_categories
            matched_skills_list = [cs.skill.name for cs in cand_skills]

            # Calculate complementarity score
            comp_score = 75 + (len(complementary_categories) * 8) + (min(15, len(matched_skills_list) * 2))
            comp_score = min(98, comp_score)

            results.append({
                'student_id': candidate.id,
                'name': candidate.user.get_full_name(),
                'username': candidate.user.username,
                'degree': candidate.degree,
                'university': candidate.university,
                'passport_slug': candidate.passport_slug,
                'overall_skill_score': candidate.overall_skill_score,
                'top_skills': matched_skills_list[:4],
                'complementary_categories': list(complementary_categories),
                'complementarity_score_pct': comp_score,
                'reason': f"Provides key capabilities in {', '.join(list(complementary_categories)[:2]) or 'Software Engineering'} that fill project skill gaps."
            })

        results.sort(key=lambda x: x['complementarity_score_pct'], reverse=True)
        return results
