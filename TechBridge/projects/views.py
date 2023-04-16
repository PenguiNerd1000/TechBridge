from django.shortcuts import render
from django.db.models import Avg
from projects.models import Project, ProjectRequest
from projects.models import Task
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm, ProjectRequestRegistrationForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from register.models import User

# Create your views here.
def projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    projects = Project.objects.all()
    avg_projects = Project.objects.all().aggregate(Avg('complete_per'))['complete_per__avg']
    tasks = Task.objects.all()
    overdue_tasks = tasks.filter(due='2')
    context = {
        'avg_projects' : avg_projects,
        'projects' : projects,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
    }
    return render(request, 'projects/projects.html', context)

# Create your views here.
def requests(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    projects = ProjectRequest.objects.filter(started=False)
    context = {
        'projects' : projects,
    }
    return render(request, 'projects/requests.html', context)

def newTask(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_task.html', context)
        else:
            return render(request, 'projects/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'projects/new_task.html', context)
    
def newProjectRequest(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    if request.method == 'POST':
        form = ProjectRequestRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRequestRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_project_request.html', context)
        else:
            return render(request, 'projects/new_project_request.html', context)
    else:
        form = ProjectRequestRegistrationForm(initial={'requester':User.objects.get(id=request.user.id)})
        context = {
            'form': form,
        }
        return render(request,'projects/new_project_request.html', context)

def newProject(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_project.html', context)
        else:
            return render(request, 'projects/new_project.html', context)
    else:
        form = ProjectRegistrationForm(initial={'requester':request.user})

        context = {
            'form': form,
        }
        return render(request,'projects/new_project.html', context)
    
def newProjectFromRequest(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_project.html', context)
        else:
            return render(request, 'projects/new_project.html', context)
    else:
        tmp = ProjectRequest.objects.get(id=id)
        form = ProjectRegistrationForm(initial={'name':tmp.name, 'description':tmp.description, 'dead_line':tmp.dead_line, 'requester': tmp.requester})
        # form.name = tmp.name
        # form.description = tmp.description
        # form.dead_line = tmp.dead_line

        context = {
            'form': form,
        }
        return render(request,'projects/new_project.html', context)