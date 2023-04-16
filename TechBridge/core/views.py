from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect
from register.models import School
from projects.models import Project
from register.models import User, Member
from projects.models import Task

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def dashboard(request):
    users = User.objects.all()
    active_users = User.objects.all().filter(is_active=True)
    schools = School.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    members = Member.objects.all()
    context = {
        'users' : users,
        'active_users' : active_users,
        'members' : members,
        'companies' : schools,
        'projects' : projects,
        'tasks' : tasks,
    }
    return render(request, 'core/dashboard.html', context)



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('core:index')
        else:
            return render(request, 'register/login.html', {'login_form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'login_form':form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:index'))


def context(request): # send context to base.html
    # if not request.session.session_key:
    #     request.session.create()
    users = User.objects.all()
    members = Member.objects.all()

    users_prof = User.objects.all()
    if request.user.is_authenticated:
        try:
            users_prof = User.objects.exclude(
                id=request.user.id)  # exclude himself from invite list
            # user_id = request.user.id
            logged_user = request.user
            friends = logged_user.friends.all()
            context = {
                'users': users,
                'users_prof': users_prof,
                'members' : members,
                'logged_user': logged_user,
                'friends' : friends,
            }
            return context
        except RuntimeError as e:
            print(e)
            users_prof = User.objects.all()
            context = {
                'users':users,
                'users_prof':users_prof,
                'members' : members,
            }
            return context
    else:
        context = {
            'users': users,
            'users_prof': users_prof,
            'members' : members,
        }
        return context
