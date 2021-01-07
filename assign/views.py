from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from users.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Notification, ProjectPhase, Project, ProjectMember, MonthlyWorkingTime
from django.contrib.auth.decorators import login_required
from . import forms
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from monthdelta import monthmod
import json


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
    for project in project_list:
        # 開始月と終了月の表示を年月に変更
        project.start_date = project.start_date.strftime('%Y-%m-%d')[:-3]
        project.end_date = project.end_date.strftime('%Y-%m-%d')[:-3]
    return render(request, 'project.html', {'project_list': project_list})


# TODO: 案件期間とメンバーの変更時の警告とMonthlyWorkingTimeの追加・削除
@login_required
def project_detailfunc(request, pk):
    if request.method == 'GET':
        # 詳細画面に渡すObjectを取得
        project_phase_list = ProjectPhase.objects.all()
        project = Project.objects.get(pk=pk)
        manager_list = User.objects.filter(is_management=True)
        staff_list = User.objects.filter(is_management=False)
        project_manager_list = project.user.filter(is_management=True)
        project_staff_list = project.user.filter(is_management=False)
        # 年月表示に修正
        project.start_date = project.start_date.strftime('%Y-%m-%d')[:-3]
        project.end_date = project.end_date.strftime('%Y-%m-%d')[:-3]

        return render(request, 'project_detail.html', {
            'project_phase_list': project_phase_list,
            'project': project,
            'manager_list': manager_list,
            'staff_list': staff_list,
            'project_manager_list': project_manager_list,
            'project_staff_list': project_staff_list,
            })

    if request.method == 'POST':
        # リクエストから入力値を取得
        name = request.POST['name']
        start_date = request.POST['start_date'] + '-01'
        end_date = request.POST['end_date'] + '-01'
        phase = request.POST['phase']
        manager = request.POST.getlist('manager')
        staff = request.POST.getlist('staff')

        input_manager = [int(s) for s in manager]
        input_staff = [int(s) for s in staff]

        # 入力情報で案件を更新
        project = Project.objects.get(pk=pk)
        project.name = name
        project.start_date = start_date
        project.end_date = end_date
        project.phase_id = phase
        project.save()

        # DBに保存されているProjectMemberを取得
        project_manager_list = project.user.filter(is_management=True)
        project_staff_list = project.user.filter(is_management=False)

        # idだけを抽出してリストを作成
        existing_manager = [item.id for item in project_manager_list]
        existing_staff = [item.id for item in project_staff_list]

        add_list = []
        delete_list = []

        #                 入力
        #           | True | False
        #      ---------------------
        #      True | None | Delete
        # 既存 ---------------------
        #      False| Add  | None
        #
        # をマネージャーとスタッフで×2

        for m in input_manager:
            if m not in existing_manager:
                add_list.append(m)

        for m in existing_manager:
            if m not in input_manager:
                delete_list.append(m)

        for s in input_staff:
            if s not in existing_staff:
                add_list.append(s)

        for s in existing_staff:
            if m not in input_staff:
                delete_list.append(s)

        print(input_manager)
        print(input_staff)
        print(existing_manager)
        print(existing_staff)
        print(add_list)
        print(delete_list)

        # ProjectMemberに保存
        for p in add_list:
            ProjectMember.objects.create(project=project, user_id=p)

        # ProjectMemberから削除
        for p in delete_list:
            # ProjectMember.objects.delete(project=project, user_id=p)
            project.user.remove(p)

        # 案件リストを取得して案件リスト画面にリダイレクト
        project_list = Project.objects.all()
        return render(request, 'project.html', {'project_list': project_list})


@login_required
def project_addfunc(request):
    if request.method == 'GET':
        project_phase_list = ProjectPhase.objects.all()
        manager_list = User.objects.filter(is_management=True)
        staff_list = User.objects.filter(is_management=False)

        return render(request, 'project_add.html', {
            'project_phase_list': project_phase_list,
            'manager_list': manager_list,
            'staff_list': staff_list,
            })

    if request.method == 'POST':
        # リクエストから入力値を取得
        name = request.POST['name']
        start_date = request.POST['start_date'] + '-01'
        end_date = request.POST['end_date'] + '-01'
        phase = request.POST['phase']
        manager =  request.POST.getlist('manager')
        staff = request.POST.getlist('staff')

        project_month_list = get_project_month(
            dt.strptime(start_date, '%Y-%m-%d'),
            dt.strptime(end_date, '%Y-%m-%d'),
        )

        # 案件を保存
        project = Project(name=name, start_date=start_date, end_date=end_date, phase_id=phase)
        project.save()

        # 案件×マネージャーでProjectMemberに保存
        for p in manager:
            project_member = ProjectMember.objects.create(project=project, user_id=p)
            # ProjectMemberごとにMonthlyWorkingTimeを一旦0埋め
            for pm in project_month_list:
                monthly_working_time = MonthlyWorkingTime(
                    project_member=project_member,
                    target_month=pm,
                    planed_working_time=0,
                    actual_working_time=0)
                monthly_working_time.save()

        # 案件×スタッフでProjectMemberに保存
        for p in staff:
            project_member = ProjectMember.objects.create(project=project, user_id=p)
            # ProjectMemberごとにMonthlyWorkingTimeを一旦0埋め
            for pm in project_month_list:
                monthly_working_time = MonthlyWorkingTime(
                    project_member=project_member,
                    target_month=pm,
                    planed_working_time=0,
                    actual_working_time=0)
                monthly_working_time.save()

        # 案件リストを取得して案件リスト画面にリダイレクト
        project_list = Project.objects.all()
        return render(request, 'project.html', {'project_list': project_list})


@login_required
def project_resourcefunc(request, pk):

    if request.method == 'GET':
        # 案件情報の取得
        project = Project.objects.get(pk=pk)
        project_member_list = ProjectMember.objects.filter(project_id=project.id)
        # print(project_member_list[0].user.username)
        project_member_id_list = [item.id for item in project_member_list]
        start_date = project.start_date
        end_date = project.end_date

        # 開始月と終了月の表示を年月に変更
        project.start_date = start_date.strftime('%Y-%m-%d')[:-3]
        project.end_date = start_date.strftime('%Y-%m-%d')[:-3]

        # 開始月と終了月から年月リストを取得
        project_month_list = get_project_month(start_date, end_date, 'year_month')

        # 案件稼働時間を取得
        monthly_working_time_list = MonthlyWorkingTime.objects.filter(project_member_id__in=project_member_id_list)
        # Date型を年月に修正
        result=[]
        for monthly_working_time in monthly_working_time_list:
            monthly_working_time.target_month = monthly_working_time.target_month.strftime('%Y-%m-%d')[:-3]

            # d = dict(monthly_working_time.target_month=int(monthly_working_time.planed_working_time - monthly_working_time.actual_working_time))
            # diff = {monthly_working_time.target_month: {monthly_working_time.project_member.user.username: int(monthly_working_time.planed_working_time - monthly_working_time.actual_working_time)}}

            # 稼働時間の予定と実績の差分をリストに格納
            list = [monthly_working_time.target_month, monthly_working_time.project_member.user.username, int(monthly_working_time.planed_working_time - monthly_working_time.actual_working_time)]
            # result.append(diff)
            result.append(list)
            # statistics=dict()
            # statistics = {monthly_working_time.project_member.user: d}
            # statistics[monthly_working_time.project_member.user].append(diff)
            # print(diff)
            print(result)

        # from django.db import connection
        # with connection.cursor() as cursor:
        #     cursor.execute("select username, target_month, (planed_working_time - actual_working_time ) from assign_monthlyworkingtime am left outer join assign_projectmember ap on am.project_member_id = ap.id left outer join users_user uu on ap.user_id = uu.id where ap.project_id = %s", [str(pk)])
        #     result = cursor.fetchall()
        #     for data in result:
        #         print(data)

        # from django.core.serializers import serialize
        # order_items = OrderItem.objects.filter(order=Order.objects.latest('id'))
        # order_items = serialize('json', project_member_list, fields=['id', 'product', 'price'])  # the fields needed for products
        #  = serialize('json', project_member_list, fields=['id', 'username'])  # the fields needed for products
        # j_project_member_list = [i['user'] for i in project_member_list.values('user')]

        # メンバー名のリストを作成
        j_project_member_list = []
        for project_member in project_member_list:
            j_project_member_list.append(project_member.user.username)

        return render(request, 'project_resource.html', {
            'project': project,
            'project_member_list': project_member_list,
            'j_project_member_list': j_project_member_list,
            'monthly_working_time_list': monthly_working_time_list,
            'project_month_list': project_month_list,
            'result': result
            })

    if request.method == 'POST':

        # 保存処理
        # print(request.POST)
        updated_list = request.POST['updated_list']
        if updated_list:
            updated_list = updated_list.split(',')

            print(updated_list)
            for item in updated_list:
                print(item)
                print(item.split('_'))
                update = item.split('_')

                # 更新対象のMonthlyWorkingTimeを取得
                monthly_working_time = MonthlyWorkingTime.objects.get(project_member=update[0], target_month=update[1]+'-01')
                print('###')
                print(update[2])
                if update[2] == 'planed':
                    monthly_working_time.planed_working_time = request.POST[item]
                else:
                    monthly_working_time.actual_working_time = request.POST[item]
                monthly_working_time.save()

        # monthly_working_time_list = MonthlyWorkingTime.objects.filter(project_member_id__in=project_member_id_list)
        # for monthly_working_time in monthly_working_time_list:
        #     monthly_working_time.target_month = monthly_working_time.target_month.strftime('%Y-%m-%d')[:-3]

        return redirect('project_resource', pk=pk)
        # return render(request, 'project_resource.html', {
        #     'project': project,
        #     'project_member_list': project_member_list,
        #     'monthly_working_time_list': monthly_working_time_list,
        #     'project_month_list': project_month_list,
        #     })



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


#  共通関数
def get_project_month(start_date, end_date, format=None):
    # ２つの日付の差を、月単位/年単位で求める -----------
    mmod = monthmod(start_date, end_date)
    # 月数差（余りは切り捨て）
    month_delta = mmod[0].months + 1
    # print(month_delta)

    project_month_list = []
    if format == 'year_month':
        for i in range(month_delta):
            project_month_list.append((start_date + relativedelta(months=i)).strftime('%Y-%m-%d')[:-3])
    else:
        for i in range(month_delta):
            project_month_list.append((start_date + relativedelta(months=i)).strftime('%Y-%m-%d'))


    # print(project_month_list)
    return project_month_list
