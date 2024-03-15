# Register your models here.
from django.contrib import admin
from .models import Project, Staff, WorkRecord
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

class StaffResource(resources.ModelResource):
    class Meta:
        model = Staff

class StaffAdmin(ImportExportModelAdmin):
    resource_class = StaffResource

class WorkRecordResource(resources.ModelResource):
    class Meta:
        model = WorkRecord

class WorkRecordAdmin(ImportExportModelAdmin):
    resource_class = WorkRecordResource

admin.site.register(Project, ProjectAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(WorkRecord, WorkRecordAdmin)