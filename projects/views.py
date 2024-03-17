from django.shortcuts import render
from .models import Project, WorkRecord, Staff

from django.db.models import Sum, F
from .models import Project, WorkRecord, Staff
from datetime import datetime

def monthly_summary(request, year, month):
    # 转换年和月为日期范围
    start_date = datetime(year=int(year), month=int(month), day=1)
    if month == '12':
        end_date = datetime(year=int(year)+1, month=1, day=1)
    else:
        end_date = datetime(year=int(year), month=int(month)+1, day=1)

    # 查询在指定日期范围内的工作记录
    work_records = WorkRecord.objects.filter(date__range=(start_date, end_date))

    # 汇总统计数据
    summary = work_records.values('project__name').annotate(
        total_hours=Sum('hours'),
        total_cost=Sum(F('hours') * F('staff__hourly_rate'))
    ).order_by('project__name')
    
    # 获取明细
    details = work_records.select_related('staff', 'project').order_by('date', 'project')

    context = {
        'summary': summary,
        'details': details,
        'year': year,
        'month': month
    }

    return render(request, 'monthly_summary.html', context)

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