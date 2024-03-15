from django.urls import path
from . import views

urlpatterns = [
    path('project_budget/', views.project_budget_view, name='project_budget'),
]