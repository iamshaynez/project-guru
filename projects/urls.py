from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_budget_view, name='project_budget'),
    path('project_budget/', views.project_budget_view, name='project_budget'),
]