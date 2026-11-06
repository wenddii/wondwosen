from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    """Developer portfolio project."""
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    short_description = models.TextField(help_text="One or two sentences describing the problem and solution.")
    highlights = models.TextField(
        blank=True,
        help_text="Enter key capabilities/features separated by newlines."
    )
    technologies = models.CharField(
        max_length=255,
        help_text="Comma-separated list of technologies (e.g. Python, Django, PostgreSQL)."
    )
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_demo_url = models.URLField(blank=True, help_text="Link to deployed application (leave blank if unavailable).")
    source_code_url = models.URLField(blank=True, help_text="Link to GitHub repository (leave blank if unavailable).")
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ordering rank for display. Lower values appear first.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def highlights_list(self):
        if not self.highlights:
            return []
        return [item.strip() for item in self.highlights.splitlines() if item.strip()]

    @property
    def tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

