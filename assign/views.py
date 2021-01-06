from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from users.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Notification, ProjectPhase, Project
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(username=username)
            return render(request, 'signup.html', {'error': 'このユーザーは登録されています。'})
        except:
            user = User.objects.create_user(username, '', password)
            return render(request, 'signup.html', {'some': 100})
    return render(request, 'signup.html')


def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            return redirect('login')
    return render(request, 'login.html')


def logoutfunc(request):
    logout(request)
    return redirect('login')


@login_required
def menufunc(request):
    return render(request, 'menu.html')


@login_required
def notificationfunc(request):
    notification_list = Notification.objects.all()
    return render(request, 'notification.html', {'notification_list': notification_list})


@login_required
def projectfunc(request):
    project_list = Project.objects.all()
    return render(request, 'project.html', {'project_list': project_list})


@login_required
def project_detailfunc(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'project_detail.html', {'project': project})


@login_required
def project_addfunc(request):
    # print('=========================')
    # print(tuple(ProjectPhase.objects.all()))
    # print('=========================')
    # form = forms.ProjectForm()

    # if request.method == 'POST':
    #     form = forms.ProjectForm(request.POST)

    # return render(request, 'project_add.html', {'form': form})

    project_phase_list = ProjectPhase.objects.all()
    manager_list = User.objects.filter(is_management=True)
    staff_list = User.objects.filter(is_management=False)

    return render(request, 'project_add.html', {
        'project_phase_list': project_phase_list,
        'manager_list': manager_list,
        'staff_list': staff_list,
        })


@login_required
def project_resourcefunc(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'project_resource.html', {'project': project})


@login_required
def memberfunc(request):
    member_list = User.objects.all()
    return render(request, 'member.html', {'member_list': member_list})


@login_required
def member_resourcefunc(request, pk):
    member = User.objects.get(pk=pk)
    return render(request, 'member_resource.html', {'member': member})


@login_required
def working_timefunc(request):
    return render(request, 'working_time.html')
