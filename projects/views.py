from django.shortcuts import render
from .models import Project, WorkRecord, Staff

from django.db.models import Sum
from .models import Project, WorkRecord, Staff


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff_members': staff_members})

def workrecord_list(request):
    work_records = WorkRecord.objects.all()
    return render(request, 'workrecord_list.html', {'work_records': work_records})

def project_budget_view(request):
    projects = Project.objects.all()
    project_data = []

    for project in projects:
        # 获取该项目的所有工作记录
        work_records = WorkRecord.objects.filter(project=project)

        # 初始化已使用预算为0
        budget_used = 0
        hours_used = 0
        for record in work_records:
            # 获取相关员工的小时费率
            staff = record.staff
            hourly_rate = staff.hourly_rate

            # 计算该工作记录的成本
            record_cost = record.hours * hourly_rate

            # 累加到已使用预算
            budget_used += record_cost
            hours_used += record.hours

        # 计算剩余预算
        budget_remaining = project.budget_amount - budget_used
        percentage = (budget_used / project.budget_amount) * 100
        percentage_str = "{:.2f}%".format(percentage)

        # 将数据添加到项目数据列表
        project_data.append({
            'project': project,
            'budget_used': budget_used,
            'budget_remaining': budget_remaining,
            'budget_total': project.budget_amount,
            'budget_percentage': percentage_str,
            'budget_man_months': project.budget_man_months,
            'hours_used': hours_used,
        })

    context = {
        'project_data': project_data
    }

    return render(request, 'project_budget.html', context)