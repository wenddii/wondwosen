from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    """View to list all projects."""
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_detail(request, slug):
    """View to display a single project detail."""
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/project_detail.html', {'project': project})

