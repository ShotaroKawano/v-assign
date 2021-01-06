from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Notification, ProjectPhase, Project, ProjectMember, MonthlyWorkingTime, DailyWorkingTime

# Register your models here.
admin.site.register(Notification)
admin.site.register(ProjectPhase)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(MonthlyWorkingTime)
admin.site.register(DailyWorkingTime)
