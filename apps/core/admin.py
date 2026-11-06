from django.contrib import admin
from .models import Profile, Technology, Experience


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'location', 'updated_at')
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'title', 'location', 'education', 'available_for_hire')
        }),
        ('Hero Section', {
            'fields': ('hero_heading', 'hero_subheading')
        }),
        ('About Section', {
            'fields': ('about_intro', 'about_full')
        }),
        ('Contact & Links', {
            'fields': ('email', 'github_url', 'linkedin_url', 'telegram_url')
        }),
        ('Media & Files', {
            'fields': ('avatar', 'cv_file')
        }),
    )

    def has_add_permission(self, request):
        # Enforce singleton pattern: only one profile instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('category', 'order', 'is_active')
    search_fields = ('name',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'period', 'order', 'is_current')
    list_editable = ('order', 'is_current')
    search_fields = ('role', 'company', 'description')

