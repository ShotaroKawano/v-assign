from django.urls import path, include
from .views import signupfunc, loginfunc, logoutfunc, menufunc, notificationfunc, projectfunc, detailfunc


urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('menu/', menufunc, name='menu'),
    path('notification/', notificationfunc, name='notification'),
    path('project/', projectfunc, name='project'),
    path('detail/<int:pk>', detailfunc, name='detail'),
]
