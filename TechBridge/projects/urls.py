from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('requests', views.requests, name='requests'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-project/<int:id>', views.newProjectFromRequest, name='new-project'),
    path('new-project-request/', views.newProjectRequest, name='new-project-request'),
    path('new-task/', views.newTask, name='new-task'),
]