from django.urls import path, include
from .views import signupfunc, loginfunc, logoutfunc, menufunc, notificationfunc, projectfunc, project_detailfunc, project_addfunc, project_resourcefunc, memberfunc, member_resourcefunc, working_timefunc


urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('menu/', menufunc, name='menu'),
    path('notification/', notificationfunc, name='notification'),
    path('project/', projectfunc, name='project'),
    path('project/<int:pk>', project_detailfunc, name='project_detail'),
    path('project/add', project_addfunc, name='project_add'),
    path('project_resource/<int:pk>', project_resourcefunc, name='project_resource'),
    path('member/', memberfunc, name='member'),
    path('member_resource/<int:pk>', member_resourcefunc, name='member_resource'),
    path('working_time/', working_timefunc, name='working_time'),
]
