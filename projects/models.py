from django.db import models

# Create your models here.
class Project(models.Model):
    project_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)
    budget_man_months = models.DecimalField(max_digits=10, decimal_places=2)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100, unique=True)
    supplier = models.CharField(max_length=100)
    onboard_date = models.DateField()
    rank = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class WorkRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # comment can be nullable
    comment = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['staff', 'date'], name='unique_work_record')
        ]