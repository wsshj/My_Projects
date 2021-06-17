from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    describe = models.CharField(default = "", max_length=100)

class Department(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    describe = models.CharField(default = "", max_length=100)

class Staff(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    passwd = models.CharField(default = "123456", max_length=20)
    sex = models.CharField(max_length=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    bossnumber =  models.IntegerField(default=0)
    bossname = models.CharField(max_length=10)
    entry_time = models.DateField()

class Project(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    # director = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name=)
    # manager = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # type = models.CharField(max_length=5)
    # state = models.CharField(max_length=5)
    # begin_time = models.DateField()
    # delivery_time = models.DateField()
    # state_description = models.CharField(max_length=256)
    # project_description = models.CharField(max_length=256)
    # member = models.ForeignKey(Staff, on_delete=models.CASCADE)

class Task(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
