from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os


def validate_image_file(image):
    """Ensure uploaded file is a valid image format and within reasonable size."""
    max_size_mb = 10
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file size must not exceed {max_size_mb}MB.")
    
    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.avif']
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported image format. Allowed formats: {', '.join(valid_extensions)}")


class ActivityCategory(models.TextChoices):
    CONTENT_CREATION = 'content_creation', 'Content Creation'
    SPORTS = 'sports', 'Sports'
    BOXING = 'boxing', 'Boxing'
    BASKETBALL = 'basketball', 'Basketball'
    CHURCH_COMMUNITY = 'church_community', 'Church & Community'
    OTHER = 'other', 'Other'


class Activity(models.Model):
    """Personal activities, hobbies, and interests beyond software development."""
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.CharField(
        max_length=40,
        choices=ActivityCategory.choices,
        default=ActivityCategory.CONTENT_CREATION,
        help_text="Primary category for this activity."
    )
    description = models.TextField(
        help_text="Short narrative or personal description of this pursuit."
    )
    content = models.TextField(
        blank=True,
        default='',
        help_text="Extended content, story, or reflections for the dedicated activity detail page."
    )
    # Social links for Content Creation (or any activity)
    tiktok_url = models.URLField(
        blank=True,
        help_text="TikTok profile URL (e.g. for Content Creation, leave blank if not applicable)."
    )
    youtube_url = models.URLField(
        blank=True,
        help_text="YouTube channel URL (e.g. for Content Creation, leave blank if not applicable)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this activity is published and visible on the website."
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which this activity appears. Lower numbers appear first."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'activity'
            slug = base_slug
            counter = 1
            while Activity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('personal:detail', kwargs={'slug': self.slug})

    @property
    def hover_photos(self):
        """Return photographs designated to appear during hover reveal."""
        hover_set = self.photos.filter(show_on_hover=True, is_published=True).order_by('display_order', 'id')
        if hover_set.exists():
            return hover_set
        return self.photos.filter(is_published=True).order_by('display_order', 'id')

    @property
    def has_hover_photos(self):
        return self.hover_photos.exists()

    @property
    def ordered_photos(self):
        return self.photos.filter(is_published=True).order_by('-is_featured', 'display_order', 'id')

    @property
    def featured_photo(self):
        """Return the explicitly featured photograph, or the first by display order."""
        featured = self.photos.filter(is_featured=True).first()
        if not featured:
            featured = self.photos.order_by('display_order', 'id').first()
        return featured

    @property
    def additional_photos(self):
        """Return supporting gallery photographs excluding the featured one."""
        featured = self.featured_photo
        if not featured:
            return self.photos.none()
        return self.photos.exclude(pk=featured.pk).order_by('display_order', 'id')

    @property
    def has_photos(self):
        return self.photos.exists()


class ActivityPhoto(models.Model):
    """Photographs associated with an activity or personal life moment."""
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
        blank=True,
        help_text="Associated activity (optional for standalone life moments)."
    )
    image = models.ImageField(
        upload_to='activities/%Y/%m/',
        validators=[validate_image_file],
        help_text="Upload high-quality photograph (JPEG, PNG, WebP)."
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional short caption or context for this photograph."
    )
    show_on_hover = models.BooleanField(
        default=True,
        help_text="Whether this photograph appears in the interactive hover reveal."
    )
    show_in_moments = models.BooleanField(
        default=False,
        help_text="Display this photograph in the 'Life Beyond the Screen' personal moments slideshow."
    )
    moments_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in the personal moments slideshow (lower numbers appear first)."
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Whether this photograph is published."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Check to make this the primary/featured photograph for the activity."
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order rank for displaying inside the activity gallery. Lower values appear first."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'display_order', 'id']
        verbose_name = 'Activity Photo'
        verbose_name_plural = 'Activity Photos'

    def __str__(self):
        title = self.activity.title if self.activity else "Personal Moment"
        caption_preview = f": {self.caption[:30]}" if self.caption else ""
        featured_badge = " [Featured]" if self.is_featured else ""
        return f"Photo for {title}{caption_preview}{featured_badge}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_featured and self.activity:
            # Enforce single featured photo per activity
            self.activity.photos.exclude(pk=self.pk).filter(is_featured=True).update(is_featured=False)


class PersonalMoment(ActivityPhoto):
    """Proxy model for dedicated Personal Moments slideshow curation in Django Admin."""
    class Meta:
        proxy = True
        verbose_name = 'Personal Moment'
        verbose_name_plural = 'Personal Moments'
        ordering = ['moments_order', 'id']
