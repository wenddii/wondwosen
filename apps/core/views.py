from django.shortcuts import render
from .models import Profile, Technology, TechnologyCategory, Experience
from apps.projects.models import Project
from apps.contact.forms import ContactForm
from apps.personal.models import Activity, ActivityPhoto


def index(request):
    """Main single-page portfolio view."""
    profile = Profile.get_profile()

    # Get active technologies grouped by category
    tech_qs = Technology.objects.filter(is_active=True).order_by('order', 'name')
    tech_grouped = {
        'Languages': tech_qs.filter(category=TechnologyCategory.LANGUAGE),
        'Frameworks': tech_qs.filter(category=TechnologyCategory.FRAMEWORK),
        'Databases': tech_qs.filter(category=TechnologyCategory.DATABASE),
        'Tools': tech_qs.filter(category=TechnologyCategory.TOOL),
    }

    # Fetch projects and experiences
    projects = Project.objects.filter(is_featured=True).order_by('order', '-created_at')
    experiences = Experience.objects.all().order_by('order', '-id')

    # Fetch published personal activities with their ordered photographs
    activities = Activity.objects.filter(is_active=True).prefetch_related('photos').order_by('display_order', 'id')

    # Fetch published personal moments for the slideshow
    moments = ActivityPhoto.objects.filter(
        show_in_moments=True,
        is_published=True
    ).select_related('activity').order_by('moments_order', 'id')

    context = {
        'profile': profile,
        'tech_grouped': tech_grouped,
        'projects': projects,
        'experiences': experiences,
        'activities': activities,
        'moments': moments,
        'contact_form': ContactForm(),
    }
    return render(request, 'core/index.html', context)

