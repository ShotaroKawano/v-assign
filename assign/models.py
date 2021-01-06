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
    start_date = models.DateField()
    end_date = models.DateField()
    # start_date = models.CharField(max_length=10)
    # end_date = models.CharField(max_length=10)
    phase = models.ForeignKey(ProjectPhase, on_delete=models.PROTECT)
    user = models.ManyToManyField(
        User,
        through="ProjectMember",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' [' + self.start_date.strftime('%Y-%m-%d')[:-3] + '-' + self.end_date.strftime('%Y-%m-%d')[:-3] + '] '


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
    target_month = models.DateField()
    planed_working_time = models.IntegerField()
    actual_working_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_member.project.name + ' | ' + self.project_member.user.username + ' | ' + self.target_month.strftime('%Y-%m-%d')[:-3]


class DailyWorkingTime(models.Model):
    """日次の稼働時間の実績"""
    project_member = models.ForeignKey(ProjectMember, default=0, on_delete=models.CASCADE)
    target_day = models.DateField()
    target_month = models.DateField()
    working_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_member + self.target_month.strftime('%Y-%m-%d')[:-3] + self.target_day.strftime('%Y-%m-%d')
