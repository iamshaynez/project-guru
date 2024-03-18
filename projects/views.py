from django.shortcuts import render
from .models import Project, WorkRecord, Staff
from django.http import JsonResponse
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

    # 汇总统计数据
    summary_vendor = work_records.values('staff__vendor').annotate(
        total_hours=Sum('hours'),
        total_cost=Sum(F('hours') * F('staff__hourly_rate'))
    ).order_by('staff__vendor')
    
    # 获取明细
    details = work_records.select_related('staff', 'project').order_by('date', 'project')

    context = {
        'summary': summary,
        'summary_vendor': summary_vendor,
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

    # Calculate the total cost of work for each project
    project_costs = WorkRecord.objects.annotate(
        total_cost=F('hours') * F('staff__hourly_rate')
    ).values('project').annotate(total_project_cost=Sum('total_cost')).order_by()

    # Create a dictionary with project id and their total costs
    project_costs_dict = {item['project']: item['total_project_cost'] for item in project_costs}

    # Calculate the remaining budget for each project and sum them up
    remaining_budget = sum(
        project.budget_amount - project_costs_dict.get(project.pk, 0)
        for project in Project.objects.all()
    )

    # Calculate the sum of all staff's hourly rate
    total_hourly_rate = Staff.objects.aggregate(sum_hourly_rate=Sum('hourly_rate'))['sum_hourly_rate']
    total_daily_rate = total_hourly_rate * 8
    total_monthly_rate = total_daily_rate * 22

    # Check if we have any staff and if the total hourly rate is not zero to avoid division by zero
    if total_hourly_rate is None or total_hourly_rate == 0:
        return JsonResponse({'error': 'No staff available or hourly rate sum is zero'}, status=400)
    # Divide the remaining budget by the sum of hourly rates to get the total available man hours
    available_man_hours = remaining_budget / total_hourly_rate

    context = {
        'project_data': project_data,
        'remaining_budget': remaining_budget,
        'total_hourly_rate': total_hourly_rate,
        'total_daily_rate': total_daily_rate,
        'total_monthly_rate': total_monthly_rate,
        'available_man_hours': available_man_hours,
        'available_man_months': available_man_hours / 22 / 8,
        'available_man_days': available_man_hours / 8
    }

    return render(request, 'project_budget.html', context)