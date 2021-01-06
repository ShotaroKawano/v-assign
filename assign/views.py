from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from users.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Notification, Project
from django.contrib.auth.decorators import login_required

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
            return redirect('list')
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
def project_resourcefunc(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'project_resource.html', {'project': project})
