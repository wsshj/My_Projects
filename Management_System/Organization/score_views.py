from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models import F
import json
import datetime

from Organization import common

from Organization.models import Score
from Organization.models import Project
from Organization.models import Staff
from Organization.models import Task

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    score_tables = json.loads(request.POST.get('score_table', default=None))

    scores = []

    for score_table in score_tables:

        response = {}

        response['project'] = score_table.get('project', None)
        response['staff'] = score_table.get('staff', None)
        response['rater'] = score_table.get('rater', None)
        response['project_weight'] = score_table.get('project_weight', None)
        response['score_weight'] = score_table.get('score_weight', None)
        response['score'] = score_table.get('score', None)
        response['date'] = score_table.get('date', None)

        if common.has_none(response):
            return HttpResponse("<p>参数错误！</p>")

        score = Score(
            project=Project.objects.get(id=response['project']),
            staff=Staff.objects.get(id=response['staff']),
            rater=Staff.objects.get(id=response['rater']),
            project_weight=response['project_weight'],
            score_weight=response['score_weight'],
            score=response['score'],
            date=response['date'],
            )
        scores.append(score)
        
    Score.objects.bulk_create(scores)

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Score.objects.filter(id=response).delete()

    return HttpResponse("<p>删除成功</p>")

def update(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['id'] = request.POST.get('id', default=None)
    response['key'] = request.POST.get('key', default=None)
    response['value'] = request.POST.get('value', default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    data = {response['key'] : response['value']}

    Score.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

# 工作台展示
def select_workbench(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    rater_id = request.POST.get('id', default=None)

    scores = Score.objects.filter(rater=rater_id).values()

    for score in scores:
        score['project_name'] = Project.objects.filter(id=score['project_id']).values().first()['name']
        score['staff_name'] = Staff.objects.filter(id=score['staff_id']).values().first()['name']
        score['date'] = score['date'].strftime('%Y-%m-%d')
        score.pop('add_date')
        score.pop('mod_date')

    data = {}
    data['response'] = list(scores)

    return HttpResponse(json.dumps(data, ensure_ascii=False))

# 项目考核展示
def select_project(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    score_id = request.POST.get('id', default=None)

    scores = Score.objects.filter(id=score_id).values()

    for score in scores:
        score['project_name'] = Project.objects.filter(id=score['project_id']).values().first()['name']
        score['staff_name'] = Staff.objects.filter(id=score['staff_id']).values().first()['name']
        score['date'] = score['date'].strftime('%Y-%m-%d')
        tasks = Task.objects.filter(project=score['project_id']).values()
        for task in tasks:
            task.pop('add_date')
            task.pop('mod_date')
        score['task'] = list(tasks)
        score.pop('add_date')
        score.pop('mod_date')
    
    data = {}
    data['response'] = list(scores)

    return HttpResponse(json.dumps(data, ensure_ascii=False))

# 月度统计展示权重和分数
def select_monthly(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    id = request.POST.get('id', default=None)
    date = request.POST.get('date', default=None)

    if date is None:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month 
    else:
        year = datetime.datetime.strptime(date, "%Y-%m-%d").year
        month = datetime.datetime.strptime(date, "%Y-%m-%d").month

    scores = Score.objects.filter(staff=id, add_date__year=year, add_date__month=month).values('project_id','project_weight').annotate(score=Sum(F('score') * F('score_weight')*0.01))

    data = {}
    data['response'] = list(scores)

    return HttpResponse(json.dumps(data, ensure_ascii=False))