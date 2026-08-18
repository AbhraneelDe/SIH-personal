import datetime
from django.core.management.base import BaseCommand
from accounts.models import User
from profiles.models import StudentProfile, RecruiterProfile, University
from skills.models import SkillCategory, Skill
from evidence.models import Evidence, SkillEvidence, EvidenceVerification
from opportunities.models import Opportunity, OpportunitySkill
from matching.services import ExplainableMatchingEngine
from teams.models import Team, TeamMember
from notifications.models import Notification

class Command(BaseCommand):
    help = "Seed database with Alex Morgan, recruiters, skills, verified evidence, and 17 demo opportunities."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting SkillPassport seed_data..."))

        # 1. Superuser / Admin
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@skillpassport.ai',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('password123')
        admin_user.save()

        # 2. Student Alex Morgan
        student_user, _ = User.objects.get_or_create(
            username='alex_morgan',
            defaults={
                'email': 'alex.morgan@stanford.edu',
                'first_name': 'Alex',
                'last_name': 'Morgan',
                'role': User.Role.STUDENT,
            }
        )
        student_user.set_password('password123')
        student_user.save()

        student_profile, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'university': 'Stanford University',
                'degree': 'B.Tech Computer Science',
                'graduation_year': 2026,
                'summary': 'Passionate AI & Full-Stack student developer with verified evidence in Python, Machine Learning, Django, and SQL.',
                'overall_skill_score': 91,
                'passport_slug': 'alex_morgan',
                'github_url': 'https://github.com/alexmorgan',
                'linkedin_url': 'https://linkedin.com/in/alexmorgan',
                'portfolio_url': 'https://alexmorgan.dev',
                'profile_completion_pct': 92,
            }
        )

        # Additional Students for Team Matching
        cand1_user, _ = User.objects.get_or_create(
            username='sarah_chen',
            defaults={'email': 'sarah@stanford.edu', 'first_name': 'Sarah', 'last_name': 'Chen', 'role': User.Role.STUDENT}
        )
        cand1_user.set_password('password123')
        cand1_user.save()
        cand1_prof, _ = StudentProfile.objects.get_or_create(
            user=cand1_user,
            defaults={'university': 'Stanford University', 'degree': 'B.S. Design & Interactive Media', 'passport_slug': 'sarah_chen', 'overall_skill_score': 89}
        )

        cand2_user, _ = User.objects.get_or_create(
            username='marcus_vance',
            defaults={'email': 'marcus@mit.edu', 'first_name': 'Marcus', 'last_name': 'Vance', 'role': User.Role.STUDENT}
        )
        cand2_user.set_password('password123')
        cand2_user.save()
        cand2_prof, _ = StudentProfile.objects.get_or_create(
            user=cand2_user,
            defaults={'university': 'MIT', 'degree': 'B.S. Cloud Systems & DevOps', 'passport_slug': 'marcus_vance', 'overall_skill_score': 94}
        )

        # 3. Recruiter Account
        rec_user, _ = User.objects.get_or_create(
            username='recruiter_techcorp',
            defaults={
                'email': 'recruiter@techcorp.example.com',
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'role': User.Role.RECRUITER,
            }
        )
        rec_user.set_password('password123')
        rec_user.save()

        rec_profile, _ = RecruiterProfile.objects.get_or_create(
            user=rec_user,
            defaults={
                'company_name': 'TechCorp AI Global',
                'industry': 'Artificial Intelligence & Cloud',
                'designation': 'Principal Technical Recruiter',
                'website': 'https://techcorp.example.com',
                'verified': True,
            }
        )

        # 4. Skill Categories & Skills
        cat_backend, _ = SkillCategory.objects.get_or_create(name='Backend & Distributed Systems')
        cat_ai, _ = SkillCategory.objects.get_or_create(name='AI, ML & Data Science')
        cat_cloud, _ = SkillCategory.objects.get_or_create(name='Cloud Engineering & DevOps')
        cat_frontend, _ = SkillCategory.objects.get_or_create(name='Frontend & UI/UX')
        cat_security, _ = SkillCategory.objects.get_or_create(name='Cybersecurity')
        cat_product, _ = SkillCategory.objects.get_or_create(name='Product & Business')

        skills_data = [
            ('Python', cat_backend, 'fa-brands fa-python'),
            ('Django', cat_backend, 'fa-solid fa-cubes'),
            ('Machine Learning', cat_ai, 'fa-solid fa-brain'),
            ('SQL', cat_backend, 'fa-solid fa-database'),
            ('Git', cat_backend, 'fa-brands fa-git-alt'),
            ('Docker', cat_cloud, 'fa-brands fa-docker'),
            ('AWS', cat_cloud, 'fa-brands fa-aws'),
            ('React', cat_frontend, 'fa-brands fa-react'),
            ('JavaScript', cat_frontend, 'fa-brands fa-js'),
            ('PyTorch', cat_ai, 'fa-solid fa-fire'),
            ('Kubernetes', cat_cloud, 'fa-solid fa-network-wired'),
            ('Cybersecurity', cat_security, 'fa-solid fa-shield-halved'),
            ('UI/UX Design', cat_frontend, 'fa-solid fa-pen-nib'),
            ('Product Management', cat_product, 'fa-solid fa-chart-line'),
        ]

        skill_objs = {}
        for sname, scat, sicon in skills_data:
            sk, _ = Skill.objects.get_or_create(name=sname, defaults={'category': scat, 'icon_name': sicon})
            skill_objs[sname] = sk

        # 5. Evidence for Alex Morgan
        ev1, _ = Evidence.objects.get_or_create(
            student=student_profile,
            title="CS106B Advanced Data Structures & Python Systems",
            defaults={
                'evidence_type': Evidence.EvidenceType.COURSEWORK,
                'issuing_organization': 'Stanford University Department of Computer Science',
                'issue_date': datetime.date(2025, 12, 10),
                'verification_status': Evidence.VerificationStatus.VERIFIED,
                'url_or_link': 'https://stanford.edu/courses/cs106b/verify/alexmorgan',
                'description': 'Mastered algorithmic complexity, Python data structures, memory models, and async IO.',
                'confidence_level': 96
            }
        )

        ev2, _ = Evidence.objects.get_or_create(
            student=student_profile,
            title="AI Resume Analyzer & Explainable Skill Matcher Project",
            defaults={
                'evidence_type': Evidence.EvidenceType.PROJECT,
                'issuing_organization': 'GitHub Open Source / Independent',
                'issue_date': datetime.date(2026, 1, 20),
                'verification_status': Evidence.VerificationStatus.VERIFIED,
                'url_or_link': 'https://github.com/alexmorgan/ai-resume-analyzer',
                'description': 'Built an end-to-end Django REST framework backend with Machine Learning skill extraction and explainable ranking engine.',
                'confidence_level': 94
            }
        )

        ev3, _ = Evidence.objects.get_or_create(
            student=student_profile,
            title="University AI Innovation Hackathon 2026 - 1st Place Winner",
            defaults={
                'evidence_type': Evidence.EvidenceType.COMPETITION,
                'issuing_organization': 'Major League Hacking (MLH) & Stanford AI Lab',
                'issue_date': datetime.date(2026, 2, 14),
                'verification_status': Evidence.VerificationStatus.VERIFIED,
                'url_or_link': 'https://devpost.com/software/campus-carbon-tracker-ai',
                'description': 'Developed Campus Carbon Tracker using Python, SQL database optimizations, and ML predictions.',
                'confidence_level': 98
            }
        )

        ev4, _ = Evidence.objects.get_or_create(
            student=student_profile,
            title="Google Cloud Digital Leader & Professional Python Certificate",
            defaults={
                'evidence_type': Evidence.EvidenceType.CREDENTIAL,
                'issuing_organization': 'Google Cloud & Python Software Foundation',
                'issue_date': datetime.date(2025, 11, 5),
                'verification_status': Evidence.VerificationStatus.VERIFIED,
                'url_or_link': 'https://www.credly.com/badges/alexmorgan-gcp',
                'description': 'Verified certification covering cloud architecture, IAM, Python microservices, and API deployment.',
                'confidence_level': 95
            }
        )

        # Verification Signatures
        for ev in [ev1, ev2, ev3, ev4]:
            EvidenceVerification.objects.get_or_create(
                evidence=ev,
                defaults={
                    'verified_by': 'SkillPassport Verification Engine & Institutional OAuth',
                    'verification_notes': 'Verified via Cryptographic Proof Signature.'
                }
            )

        # Attach Evidence to Skill Evidence mapping for Alex Morgan
        alex_skills_spec = [
            ('Python', 92, SkillEvidence.ProficiencyLevel.ADVANCED, [ev1, ev2, ev3, ev4]),
            ('Django', 86, SkillEvidence.ProficiencyLevel.ADVANCED, [ev2]),
            ('Machine Learning', 84, SkillEvidence.ProficiencyLevel.ADVANCED, [ev2, ev3]),
            ('SQL', 85, SkillEvidence.ProficiencyLevel.ADVANCED, [ev1, ev3]),
            ('Git', 91, SkillEvidence.ProficiencyLevel.EXPERT, [ev2, ev3]),
            ('JavaScript', 78, SkillEvidence.ProficiencyLevel.INTERMEDIATE, [ev2]),
        ]

        for sname, score, prof, ev_list in alex_skills_spec:
            sk = skill_objs[sname]
            se, _ = SkillEvidence.objects.get_or_create(
                student=student_profile,
                skill=sk,
                defaults={'score_pct': score, 'proficiency': prof}
            )
            se.evidences.set(ev_list)

        # Also add skills for candidates
        se_c1, _ = SkillEvidence.objects.get_or_create(student=cand1_prof, skill=skill_objs['UI/UX Design'], defaults={'score_pct': 94, 'proficiency': SkillEvidence.ProficiencyLevel.EXPERT})
        se_c1b, _ = SkillEvidence.objects.get_or_create(student=cand1_prof, skill=skill_objs['React'], defaults={'score_pct': 88, 'proficiency': SkillEvidence.ProficiencyLevel.ADVANCED})
        
        se_c2, _ = SkillEvidence.objects.get_or_create(student=cand2_prof, skill=skill_objs['Docker'], defaults={'score_pct': 96, 'proficiency': SkillEvidence.ProficiencyLevel.EXPERT})
        se_c2b, _ = SkillEvidence.objects.get_or_create(student=cand2_prof, skill=skill_objs['AWS'], defaults={'score_pct': 92, 'proficiency': SkillEvidence.ProficiencyLevel.ADVANCED})

        # 6. 17 Realistic Demo Opportunities
        opportunities_list = [
            ("AI/ML Engineering Intern", "TechCorp AI Global", Opportunity.Category.INTERNSHIP, "Build high-throughput Python inference APIs and train transformer models.", "San Francisco, CA", Opportunity.LocationType.HYBRID, "$4,500 / month", ["Python", "Machine Learning", "SQL", "Git"], ["Docker", "AWS"]),
            ("Full Stack Developer Intern", "Innovate Labs", Opportunity.Category.INTERNSHIP, "Develop customer-facing web platforms with Django and modern frontend JavaScript frameworks.", "Remote", Opportunity.LocationType.REMOTE, "$4,000 / month", ["Python", "Django", "JavaScript", "SQL"], ["Git", "React"]),
            ("Python Backend Developer Intern", "MicroStream FinTech", Opportunity.Category.INTERNSHIP, "Design scalable microservices, RESTful APIs, and database migrations.", "New York, NY", Opportunity.LocationType.HYBRID, "$4,200 / month", ["Python", "Django", "SQL", "Git"], ["Docker"]),
            ("Data Science Intern", "DataPulse Analytics", Opportunity.Category.INTERNSHIP, "Perform exploratory analysis, build statistical ML models, and visualize dataset metrics.", "Austin, TX", Opportunity.LocationType.HYBRID, "$3,800 / month", ["Python", "Machine Learning", "SQL"], ["PyTorch"]),
            ("Cloud Engineering Intern", "CloudScale Systems", Opportunity.Category.INTERNSHIP, "Deploy automated CI/CD container workloads and configure AWS infrastructure.", "Seattle, WA", Opportunity.LocationType.HYBRID, "$4,800 / month", ["Docker", "AWS", "Git"], ["Python", "Kubernetes"]),
            ("Backend Developer Intern", "OmniScale Inc", Opportunity.Category.INTERNSHIP, "Maintain distributed service architectures, caching pipelines, and SQL databases.", "Remote", Opportunity.LocationType.REMOTE, "$3,900 / month", ["Python", "SQL", "Git"], ["Django"]),
            ("Cybersecurity Research Intern", "ShieldX Security", Opportunity.Category.RESEARCH, "Audit API authorization vulnerability patterns and implement security logging.", "Boston, MA", Opportunity.LocationType.ON_SITE, "$4,100 / month", ["Cybersecurity", "Python", "Git"], ["Docker"]),
            ("Frontend Developer Intern", "PixelCraft Interactive", Opportunity.Category.INTERNSHIP, "Construct accessible UI component systems using modern JavaScript and React.", "Remote", Opportunity.LocationType.REMOTE, "$3,600 / month", ["JavaScript", "React", "UI/UX Design"], ["Git"]),
            ("Product Engineering Intern", "NextGen SaaS", Opportunity.Category.INTERNSHIP, "Integrate user telemetry, product analytics, and customer feature flows.", "San Jose, CA", Opportunity.LocationType.HYBRID, "$4,200 / month", ["Python", "JavaScript", "Product Management"], ["SQL"]),
            ("Data Analyst Intern", "Quantum Metrics", Opportunity.Category.INTERNSHIP, "Transform complex logs into executive dashboards and relational database queries.", "Chicago, IL", Opportunity.LocationType.HYBRID, "$3,500 / month", ["SQL", "Python"], ["Machine Learning"]),
            ("DevOps & Infrastructure Intern", "AutoDeploy Corp", Opportunity.Category.INTERNSHIP, "Orchestrate Kubernetes clusters and Docker container deployment pipelines.", "Remote", Opportunity.LocationType.REMOTE, "$4,600 / month", ["Docker", "Kubernetes", "AWS", "Git"], ["Python"]),
            ("Computer Vision Research Intern", "AeroSpatial AI", Opportunity.Category.RESEARCH, "Train convolutional networks for real-time object detection and spatial tracking.", "Palo Alto, CA", Opportunity.LocationType.ON_SITE, "$5,000 / month", ["Python", "Machine Learning", "PyTorch"], ["Docker"]),
            ("NLP Research Intern", "LinguistAI Research", Opportunity.Category.RESEARCH, "Fine-tune LLM embeddings for structured entity extraction and sentiment analysis.", "Remote", Opportunity.LocationType.REMOTE, "$4,700 / month", ["Python", "Machine Learning", "PyTorch"], ["Git"]),
            ("Software Engineering Intern", "OpenCore Systems", Opportunity.Category.INTERNSHIP, "Contribute to core open-source Python libraries, bug triage, and regression tests.", "Remote", Opportunity.LocationType.REMOTE, "$4,000 / month", ["Python", "Git", "SQL"], ["Django"]),
            ("AI Product Management Intern", "VentureLabs Accelerator", Opportunity.Category.INTERNSHIP, "Conduct market feasibility analysis and define product requirements for AI startups.", "San Francisco, CA", Opportunity.LocationType.HYBRID, "$3,700 / month", ["Product Management", "Python"], ["UI/UX Design"]),
            ("Open Source Engineering Internship", "Apache Software Foundation", Opportunity.Category.INTERNSHIP, "Build community infrastructure tools and test suites for high-scale databases.", "Remote", Opportunity.LocationType.REMOTE, "$3,800 / month", ["Python", "Git", "SQL"], ["Docker"]),
            ("Multidisciplinary Innovation Team", "Smart Campus AI Project", Opportunity.Category.TEAM_OPPORTUNITY, "Join a 4-person multidisciplinary team building smart campus IoT energy optimization.", "Stanford Campus", Opportunity.LocationType.HYBRID, "Project Grant $10,000", ["Python", "Machine Learning", "React", "Docker"], ["AWS", "UI/UX Design"]),
        ]

        for title, org, cat, desc, loc, loctype, stipend, req_skills, pref_skills in opportunities_list:
            opp, _ = Opportunity.objects.get_or_create(
                title=title,
                organization=org,
                defaults={
                    'recruiter': rec_profile,
                    'category': cat,
                    'description': desc,
                    'location': loc,
                    'location_type': loctype,
                    'duration': "3 - 6 Months",
                    'stipend': stipend,
                    'application_deadline': datetime.date(2026, 12, 31)
                }
            )

            for sname in req_skills:
                if sname in skill_objs:
                    OpportunitySkill.objects.get_or_create(
                        opportunity=opp,
                        skill=skill_objs[sname],
                        defaults={'requirement_type': OpportunitySkill.SkillRequirementType.REQUIRED, 'min_proficiency_score': 75}
                    )

            for sname in pref_skills:
                if sname in skill_objs:
                    OpportunitySkill.objects.get_or_create(
                        opportunity=opp,
                        skill=skill_objs[sname],
                        defaults={'requirement_type': OpportunitySkill.SkillRequirementType.PREFERRED, 'min_proficiency_score': 65}
                    )

            # Pre-calculate match score for Alex Morgan
            ExplainableMatchingEngine.calculate_match(student_profile, opp)

        # 7. Seed Team
        team1, _ = Team.objects.get_or_create(
            title="Smart Campus AI Project",
            defaults={
                'description': 'Building an automated energy prediction engine combining backend AI microservices with responsive UI.',
                'leader': student_profile,
                'complementarity_score': 94
            }
        )
        TeamMember.objects.get_or_create(team=team1, student=student_profile, defaults={'role': TeamMember.RoleInTeam.LEADER})
        TeamMember.objects.get_or_create(team=team1, student=cand1_prof, defaults={'role': TeamMember.RoleInTeam.FRONTEND})
        TeamMember.objects.get_or_create(team=team1, student=cand2_prof, defaults={'role': TeamMember.RoleInTeam.CLOUD})

        # 8. Seed Notifications
        Notification.objects.get_or_create(
            user=student_user,
            title="Python Credential Verified",
            defaults={'message': 'Your Stanford CS106B coursework certificate has been verified via institutional signature.', 'notification_type': Notification.NotificationType.VERIFICATION, 'link_url': '/evidence/manage/'}
        )
        Notification.objects.get_or_create(
            user=student_user,
            title="92% Opportunity Match Found",
            defaults={'message': 'You have a 92% evidence match for AI/ML Engineering Intern at TechCorp AI Global.', 'notification_type': Notification.NotificationType.MATCH, 'link_url': '/opportunities/'}
        )
        Notification.objects.get_or_create(
            user=student_user,
            title="Skill Gap Alert: Docker & AWS",
            defaults={'message': 'Strengthen Docker containerization and AWS cloud deployment to boost your match for Cloud Engineer roles.', 'notification_type': Notification.NotificationType.SKILL_GAP, 'link_url': '/skill-gaps/'}
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded SkillPassport with Alex Morgan, recruiters, skills, verified evidence, and 17 realistic opportunities!"))
