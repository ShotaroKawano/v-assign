from django.urls import path, include
from .views import signupfunc, loginfunc, logoutfunc, menufunc, notificationfunc, projectfunc, project_detailfunc, project_resourcefunc


urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('menu/', menufunc, name='menu'),
    path('notification/', notificationfunc, name='notification'),
    path('project/', projectfunc, name='project'),
    path('project/<int:pk>', project_detailfunc, name='project_detail'),
    path('project_resource/<int:pk>', project_resourcefunc, name='project_resource'),
]
