from django.db import models
from users.models import User

# Create your models here.

class Notification(models.Model):
    """通知"""
    content = models.CharField(max_length=200)
    is_checked = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[Alert] ' + self.content



class ProjectPhase(models.Model):
    """案件のフェーズ"""
    phase = models.CharField(max_length=20)

    def __str__(self):
        return self.phase


class Project(models.Model):
    """案件"""
    name = models.CharField(max_length=200)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    phase = models.ForeignKey(ProjectPhase, on_delete=models.PROTECT)
    user = models.ManyToManyField(
        User,
        through="ProjectMember",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' [' + self.start_date + '-' + self.end_date + '] '


class ProjectMember(models.Model):
    """案件×メンバー"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="project_member_unique"
            ),
        ]


    def __str__(self):
        return self.project.name + ' | ' + self.user.username


class MonthlyWorkingTime(models.Model):
    """月次の稼働時間の予定と実績"""
    project_member = models.ForeignKey(ProjectMember, default=0, on_delete=models.CASCADE)
    target_month = models.IntegerField()
    planed_working_time = models.IntegerField()
    actual_working_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_member.project.name + ' | ' + self.project_member.user.username + ' | ' + self.target_month


class DailyWorkingTime(models.Model):
    """日次の稼働時間の実績"""
    project_member = models.ForeignKey(ProjectMember, default=0, on_delete=models.CASCADE)
    target_day = models.IntegerField()
    target_month = models.IntegerField()
    working_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_member + self.target_month + self.target_day
