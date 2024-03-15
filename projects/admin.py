# Register your models here.
from django.contrib import admin
from django import forms
from .models import Project, Staff, WorkRecord
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project

class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('project_number', 'name', 'budget_man_months', 'budget_amount', 'comment')
    resource_class = ProjectResource

class StaffResource(resources.ModelResource):
    class Meta:
        model = Staff

class StaffAdmin(ImportExportModelAdmin):
    list_display = ('name', 'supplier', 'onboard_date', 'rank', 'hourly_rate', 'comment')
    resource_class = StaffResource

class WorkRecordResource(resources.ModelResource):
    staff__name = resources.Field(attribute='staff__name')
    project__name = resources.Field(attribute='project__name')

    class Meta:
        model = WorkRecord
        fields = ('id', 'staff__name', 'date', 'hours', 'project__name', 'comment')
        export_order = ('id', 'staff__name', 'date', 'hours', 'project__name', 'comment')

    def dehydrate_staff__name(self, obj):
        return obj.staff.name

    def dehydrate_project__name(self, obj):
        return obj.project.name

class WorkRecordForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), to_field_name="name")
    staff = forms.ModelChoiceField(queryset=Staff.objects.all(), to_field_name="name")

    class Meta:
        model = WorkRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].label_from_instance = self.label_from_instance
        self.fields['staff'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return str(obj)

class WorkRecordAdmin(ImportExportModelAdmin):
    list_display = ('staff_name', 'date', 'hours', 'project_name', 'comment')

    def staff_name(self, obj):
        return obj.staff.name

    def project_name(self, obj):
        return obj.project.name
    
    staff_name.short_description = 'Staff Name'
    project_name.short_description = 'Project Name'
    form = WorkRecordForm
    resource_class = WorkRecordResource

admin.site.register(Project, ProjectAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(WorkRecord, WorkRecordAdmin)