from django.db import models
from users.models import User

# Create your models here.

class Notification(models.Model):
    content = models.CharField(max_length=200)
    is_checked = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectPhase(models.Model):
    phase = models.CharField(max_length=20)


class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    phase = models.ForeignKey(ProjectPhase, on_delete=models.PROTECT)
    user = models.ManyToManyField(
        User,
        through="ProjectMember",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_management = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


class MonthlyWorkingTime(models.Model):
    target_month = models.CharField(max_length=10)
    planed_working_time = models.IntegerField()
    actual_working_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DailyWorkingTime(models.Model):
    target_day = models.CharField(max_length=10)
    target_month = models.CharField(max_length=10)
    working_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
