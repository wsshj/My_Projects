from datetime import time
from django.db import models
import django.utils.timezone as timezone
from django.core import serializers

# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField(default=-1)
    describe = models.CharField(default = "", max_length=100)

class Department(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField(default=-1)
    describe = models.CharField(default = "", max_length=100)

class Matter(models.Model):
    name = models.CharField(max_length=30)

class Staff(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    passwd = models.CharField(default = "123456", max_length=20)
    sex = models.CharField(max_length=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    boss_id =  models.IntegerField(default=0)
    boss_name = models.CharField(max_length=10)
    entry_time = models.DateField()
    phone = models.CharField(max_length=11)
    add_date = models.DateTimeField('保存日期', default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)
    
class Project(models.Model):
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, default=1)
    director = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_director', default=-1)
    manager = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_manager', default=-1)
    type = models.CharField(max_length=25, default='')
    state = models.CharField(max_length=25, default='')
    begin_time = models.DateField(default='2000-01-01')
    delivery_time = models.DateField(default='2000-01-01')
    state_description = models.CharField(max_length=256, default='')
    project_description = models.CharField(max_length=256, default='')
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)  
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

class Task(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1)
    state = models.CharField(max_length=5)
    progress = models.FloatField(max_length=5)
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

class Daily(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time = models.FloatField(max_length=5)
    progress = models.FloatField(max_length=5)
    content = models.CharField(max_length=256)
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

# class Achievements(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     weight = models.IntegerField(default=0)
#     rater_50 = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_rater_50')
#     rater_30 = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_rater_30')
#     rater_20 = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_rater_20')
#     date = models.DateField()
#     add_date = models.DateTimeField('保存日期',default = timezone.now)
#     mod_date = models.DateTimeField('最后修改日期', auto_now = True)

class Score(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1)
    rater = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1, related_name='staff_rater')
    project_weight = models.IntegerField(default=0)
    score_weight = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    date = models.DateField(default="2000-01-01")
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

class ScoreMember(models.Model):
    name = models.CharField(max_length=30)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1)
    rater = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1, related_name='ScoreMember_rater')
    weight = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)