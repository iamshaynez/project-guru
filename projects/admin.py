# Register your models here.
from django.contrib import admin 
from rangefilter.filters import DateRangeFilter
from django import forms
from .models import Project, Staff, WorkRecord
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project

class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('project_number', 'name', 'budget_man_months', 'budget_amount', 'active', 'comment')
    list_filter = ('active','name')
    resource_class = ProjectResource

class StaffResource(resources.ModelResource):
    class Meta:
        model = Staff

class StaffAdmin(ImportExportModelAdmin):
    list_display = ('name', 'name_cn', 'vendor','onboard_date', 'rank', 'hourly_rate', 'active', 'comment')
    list_filter = ('vendor', 'rank', ('onboard_date', DateRangeFilter), 'active')
    resource_class = StaffResource


class StaffForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        print(f'clean staff key: {value}')
        return self.model.objects.get_or_create(name=value)[0]

class ProjectForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        print(f'clean project key: {value}')
        return self.model.objects.get_or_create(project_number=value)[0]


class WorkRecordResource(resources.ModelResource):
    staff = fields.Field(
        column_name='staff',
        attribute='staff',
        widget=StaffForeignKeyWidget(Staff, 'name')
    )

    project = fields.Field(
        column_name='project',
        attribute='project',
        widget=ProjectForeignKeyWidget(Project, 'project_number')
    )

    class Meta:
        model = WorkRecord
        skip_unchanged = True
        fields = ('id', 'staff', 'date', 'hours', 'project', 'comment')
        export_order = ('id', 'staff', 'date', 'hours', 'project', 'comment')

class WorkRecordAdmin(ImportExportModelAdmin):
    list_display = ('staff_name', 'date', 'hours', 'project_number', 'comment')
    list_filter = ('staff', ('date', DateRangeFilter), 'project')  # 你希望能够筛选的字段

    def staff_name(self, obj):
        return obj.staff.name

    def project_number(self, obj):
        return obj.project.project_number
    
    staff_name.short_description = 'Staff Name'
    project_number.short_description = 'Project Number'

    resource_class = WorkRecordResource

admin.site.register(Project, ProjectAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(WorkRecord, WorkRecordAdmin)