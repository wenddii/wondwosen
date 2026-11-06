from django.contrib import admin
from django.utils.html import format_html
from .models import Activity, ActivityPhoto, PersonalMoment


class ActivityPhotoInline(admin.TabularInline):
    model = ActivityPhoto
    extra = 1
    fields = ('thumbnail_preview', 'image', 'caption', 'show_on_hover', 'show_in_moments', 'moments_order', 'is_featured', 'display_order')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 75px; height: 55px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "No image"
    thumbnail_preview.short_description = "Preview"


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'display_order', 'is_active', 'photo_count', 'updated_at')
    list_editable = ('display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ActivityPhotoInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Dedicated Detail Page Content', {
            'fields': ('content',),
            'description': 'Extended narrative, reflections, or notes for this activity’s dedicated detail page.'
        }),
        ('Social Profiles (Content Creation)', {
            'fields': ('tiktok_url', 'youtube_url'),
            'description': 'Configure TikTok profile and YouTube channel URLs.'
        }),
        ('Visibility & Ordering', {
            'fields': ('is_active', 'display_order')
        }),
    )

    def photo_count(self, obj):
        total = obj.photos.count()
        hover = obj.photos.filter(show_on_hover=True).count()
        if total > 0:
            return format_html('{} total ({} on hover)', total, hover)
        return "0 photos"
    photo_count.short_description = "Photos"

    actions = ['make_published', 'make_hidden']

    def make_published(self, request, queryset):
        queryset.update(is_active=True)
    make_published.short_description = "Publish selected activities"

    def make_hidden(self, request, queryset):
        queryset.update(is_active=False)
    make_hidden.short_description = "Hide selected activities"


@admin.register(ActivityPhoto)
class ActivityPhotoAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'caption', 'activity', 'show_on_hover', 'show_in_moments', 'moments_order', 'is_published', 'uploaded_at')
    list_filter = ('show_in_moments', 'show_on_hover', 'is_published', 'activity')
    list_editable = ('show_in_moments', 'moments_order', 'show_on_hover', 'is_published')
    search_fields = ('caption', 'activity__title')

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 45px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "No image"
    thumbnail_preview.short_description = "Preview"


@admin.register(PersonalMoment)
class PersonalMomentAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'caption', 'moments_order', 'show_in_moments', 'is_published', 'activity', 'uploaded_at')
    list_editable = ('moments_order', 'show_in_moments', 'is_published')
    list_filter = ('show_in_moments', 'is_published', 'activity')
    search_fields = ('caption', 'activity__title')
    fieldsets = (
        ('Photograph & Caption', {
            'fields': ('image', 'caption', 'activity'),
            'description': 'Upload photograph depicting life moments (boxing, basketball, university life, church, public speaking, etc.).'
        }),
        ('Slideshow Configuration', {
            'fields': ('show_in_moments', 'moments_order', 'is_published'),
            'description': 'Control display in the "Life Beyond the Screen" automatic photo slideshow.'
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 75px; height: 55px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "No image"
    thumbnail_preview.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        if not change and not obj.show_in_moments:
            obj.show_in_moments = True
        super().save_model(request, obj, form, change)
