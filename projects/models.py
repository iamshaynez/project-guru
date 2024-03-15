from django.db import models

# Create your models here.
class Project(models.Model):
    project_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    budget_man_months = models.DecimalField(max_digits=10, decimal_places=2)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField()

class Staff(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100)
    onboard_date = models.DateField()
    rank = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField()

class WorkRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField()