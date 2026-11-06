from django.db import models


class Profile(models.Model):
    """Personal profile identity and contact metadata."""
    name = models.CharField(max_length=100, default='Wendwosen Tessema')
    title = models.CharField(max_length=150, default='Software Developer | Backend Engineer | Tech Entrepreneur')
    location = models.CharField(max_length=100, default='Bahir Dar, Ethiopia')
    education = models.CharField(max_length=200, default='Information Systems, Bahir Dar University')
    hero_heading = models.CharField(max_length=200, default="Hi, I'm Wendwosen.")
    hero_subheading = models.CharField(
        max_length=300,
        default="I'm a software developer building practical digital solutions and business systems."
    )
    about_intro = models.TextField(
        default=(
            "I'm a software developer and aspiring tech entrepreneur interested in "
            "building practical software solutions that solve real-world problems. "
            "I enjoy turning ideas into working products, developing backend systems, "
            "and exploring how technology can improve businesses and everyday life."
        )
    )
    about_full = models.TextField(
        default=(
            "Currently studying Information Systems at Bahir Dar University, my work bridges the gap "
            "between robust backend engineering and real-world business needs. I have hands-on experience "
            "designing databases, architecting modular Django backends, and building enterprise systems—from "
            "retail ERPs to university registration platforms.\n\n"
            "As a co-founder at Harbe Digital Solutions, I collaborate directly with businesses to understand "
            "their operational bottlenecks and turn them into elegant software solutions. I thrive in environments "
            "where code has immediate utility, clean architecture matters, and every feature serves a distinct purpose."
        )
    )
    email = models.EmailField(default='wendwosentessema@gmail.com')
    github_url = models.URLField(default='https://github.com')
    linkedin_url = models.URLField(default='https://linkedin.com')
    telegram_url = models.URLField(default='https://t.me')
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_file = models.FileField(upload_to='documents/', blank=True, null=True)
    available_for_hire = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.name

    @classmethod
    def get_profile(cls):
        """Retrieve existing profile or create the default one."""
        profile, _ = cls.objects.get_or_create(id=1)
        return profile


class TechnologyCategory(models.TextChoices):
    LANGUAGE = 'language', 'Language'
    FRAMEWORK = 'framework', 'Framework'
    DATABASE = 'database', 'Database'
    TOOL = 'tool', 'Tool'


class Technology(models.Model):
    """Categorized technologies and tools."""
    name = models.CharField(max_length=60)
    category = models.CharField(
        max_length=20,
        choices=TechnologyCategory.choices,
        default=TechnologyCategory.LANGUAGE
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    """Timeline entry for work experience, founding roles, and internships."""
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    company_url = models.URLField(blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    period = models.CharField(max_length=100)
    description = models.TextField(help_text="Short factual description of responsibilities and achievements.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        return f"{self.role} at {self.company}"

