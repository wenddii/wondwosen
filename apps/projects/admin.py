from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_featured', 'technologies', 'created_at')
    list_editable = ('order', 'is_featured')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'technologies', 'highlights')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'highlights', 'technologies')
        }),
        ('Media & Links', {
            'fields': ('image', 'live_demo_url', 'source_code_url')
        }),
        ('Visibility & Ordering', {
            'fields': ('is_featured', 'order')
        }),
    )

