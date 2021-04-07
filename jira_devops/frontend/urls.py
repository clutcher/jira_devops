from django.urls import path

from jira_devops.frontend import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('frames/releases/', views.ReleaseView.as_view()),
]
