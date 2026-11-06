from django.shortcuts import render, get_object_or_404
from .models import Activity


def activity_list(request):
    """List all published activities."""
    activities = Activity.objects.filter(is_active=True).prefetch_related('photos').order_by('display_order', 'id')
    return render(request, 'personal/activity_list.html', {'activities': activities})


def activity_detail(request, slug):
    """Detail view for a single activity."""
    activity = get_object_or_404(Activity, slug=slug, is_active=True)
    return render(request, 'personal/activity_detail.html', {'activity': activity})

