from django.urls import path
from . import views

app_name = 'personal'

urlpatterns = [
    path('', views.activity_list, name='list'),
    path('<slug:slug>/', views.activity_detail, name='detail'),
]

