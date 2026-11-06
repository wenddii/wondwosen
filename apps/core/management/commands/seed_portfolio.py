from django.core.management.base import BaseCommand
from apps.core.models import Profile, Technology, TechnologyCategory, Experience
from apps.projects.models import Project


class Command(BaseCommand):
    help = 'Seeds initial portfolio content (profile, projects, experience, technologies)'

    def handle(self, *args, **options):
        self.stdout.write('Seeding portfolio data...')

        # 1. Profile
        profile, created = Profile.objects.get_or_create(id=1)
        profile.name = 'Wendwosen Tessema'
        profile.title = 'Software Developer | Backend Engineer | Tech Entrepreneur'
        profile.location = 'Bahir Dar, Ethiopia'
        profile.education = 'Information Systems, Bahir Dar University'
        profile.hero_heading = "Hi, I'm Wendwosen."
        profile.hero_subheading = "I'm a software developer building practical digital solutions and business systems."
        profile.about_intro = (
            "I'm a software developer and aspiring tech entrepreneur interested in "
            "building practical software solutions that solve real-world problems. "
            "I enjoy turning ideas into working products, developing backend systems, "
            "and exploring how technology can improve businesses and everyday life."
        )
        profile.about_full = (
            "Currently studying Information Systems at Bahir Dar University, my work bridges the gap "
            "between robust backend engineering and real-world business needs. I have hands-on experience "
            "designing databases, architecting modular Django backends, and building enterprise systems—from "
            "retail ERPs to university registration platforms.\n\n"
            "As a co-founder at Harbe Digital Solutions, I collaborate directly with businesses to understand "
            "their operational bottlenecks and turn them into elegant software solutions. I thrive in environments "
            "where code has immediate utility, clean architecture matters, and every feature serves a distinct purpose."
        )
        profile.email = 'wendwosentessema@gmail.com'
        profile.github_url = 'https://github.com'
        profile.linkedin_url = 'https://linkedin.com'
        profile.telegram_url = 'https://t.me'
        profile.save()
        self.stdout.write(self.style.SUCCESS('Profile initialized.'))

        # 2. Technologies
        tech_data = [
            # Languages
            ('Python', TechnologyCategory.LANGUAGE, 1),
            ('JavaScript', TechnologyCategory.LANGUAGE, 2),
            ('Go', TechnologyCategory.LANGUAGE, 3),
            ('HTML', TechnologyCategory.LANGUAGE, 4),
            ('CSS', TechnologyCategory.LANGUAGE, 5),
            # Frameworks
            ('Django', TechnologyCategory.FRAMEWORK, 1),
            ('Django REST Framework', TechnologyCategory.FRAMEWORK, 2),
            # Databases
            ('PostgreSQL', TechnologyCategory.DATABASE, 1),
            ('SQLite', TechnologyCategory.DATABASE, 2),
            # Tools
            ('Git', TechnologyCategory.TOOL, 1),
            ('GitHub', TechnologyCategory.TOOL, 2),
            ('Docker', TechnologyCategory.TOOL, 3),
            ('Cloudinary', TechnologyCategory.TOOL, 4),
        ]

        for name, category, order in tech_data:
            Technology.objects.update_or_create(
                name=name,
                category=category,
                defaults={'order': order, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS(f'{len(tech_data)} technologies seeded.'))

        # 3. Projects
        projects_data = [
            {
                'title': 'NOAH Mini Market ERP',
                'slug': 'noah-mini-market-erp',
                'short_description': 'Comprehensive retail enterprise resource planning system tailored for local grocery and supermarket management.',
                'highlights': "Inventory management\nSales tracking\nCash management\nBusiness dashboard",
                'technologies': 'Python, Django, PostgreSQL, HTML, CSS',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'CampusCore',
                'slug': 'campuscore',
                'short_description': 'Specialized university non-cafeteria student registration and verification platform.',
                'highlights': "University non-cafeteria student registration system\nStudent verification\nRegistration management\nAdministrative dashboard",
                'technologies': 'Python, Django, SQLite, HTML, CSS',
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Harbe Digital Solutions',
                'slug': 'harbe-digital-solutions',
                'short_description': 'Digital agency platform offering custom software systems, client websites, and tech consulting.',
                'highlights': "Digital solutions business\nBusiness websites\nCustom software systems",
                'technologies': 'Python, Django, PostgreSQL, JavaScript, Docker',
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'Delala',
                'slug': 'delala',
                'short_description': 'Dynamic marketplace platform connecting buyers and sellers with secure authentication and robust listing APIs.',
                'highlights': "Marketplace platform\nBackend API\nAuthentication and database management",
                'technologies': 'Python, Django REST Framework, PostgreSQL, Docker',
                'is_featured': True,
                'order': 4,
            },
            {
                'title': 'Africa Barbershop',
                'slug': 'africa-barbershop',
                'short_description': 'Modern appointment booking and shop management system integrated with instant Telegram notifications.',
                'highlights': "Barbershop management and booking\nTelegram notifications",
                'technologies': 'Python, Django, SQLite, Telegram Bot API',
                'is_featured': True,
                'order': 5,
            },
        ]

        for p_data in projects_data:
            Project.objects.update_or_create(
                slug=p_data['slug'],
                defaults=p_data
            )
        self.stdout.write(self.style.SUCCESS(f'{len(projects_data)} projects seeded.'))

        # 4. Experience
        experiences_data = [
            {
                'role': 'Co-founder, Technology & Product',
                'company': 'Harbe Digital Solutions',
                'company_url': '',
                'location': 'Bahir Dar, Ethiopia',
                'period': '2024 — Present',
                'description': 'Leading technical architecture, product design, and delivery of client business systems and digital solutions.',
                'order': 1,
                'is_current': True,
            },
            {
                'role': 'Freelance Software Developer',
                'company': 'Independent Practice',
                'company_url': '',
                'location': 'Bahir Dar, Ethiopia',
                'period': '2023 — Present',
                'description': 'Designing and implementing bespoke web applications, database schemas, and business management tools for SMEs.',
                'order': 2,
                'is_current': True,
            },
            {
                'role': 'Software Development Intern',
                'company': 'Ethio Telecom',
                'company_url': 'https://www.ethiotelecom.et',
                'location': 'Ethiopia',
                'period': '2024',
                'description': 'Gained practical industry experience in enterprise telecommunications software systems, services, and backend workflows.',
                'order': 3,
                'is_current': False,
            },
        ]

        for exp in experiences_data:
            Experience.objects.update_or_create(
                role=exp['role'],
                company=exp['company'],
                defaults=exp
            )
        self.stdout.write(self.style.SUCCESS(f'{len(experiences_data)} experiences seeded.'))

        self.stdout.write(self.style.SUCCESS('All portfolio seed data successfully configured!'))

