from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime

from Organization import common

from Organization.models import ScoreMember
from Organization.models import Project
from Organization.models import Staff
from Organization.models import Task

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    score_tables = json.loads(request.POST.get('score_table', default=None))

    score_members = []

    for score_table in score_tables:

        response = {}

        response['name'] = score_table.get('name', None)
        response['staff'] = score_table.get('staff', None)
        response['rater'] = score_table.get('rater', None)
        response['weight'] = score_table.get('weight', None)
        response['score'] = score_table.get('score', None)

        if common.has_none(response):
            return HttpResponse("<p>参数错误！</p>")

        score_member = ScoreMember(
            name=response['name'],
            staff=Staff.objects.get(id=response['staff']),
            rater=Staff.objects.get(id=response['rater']),
            weight=response['weight'],
            score=response['score'],
            )
        score_members.append(score_member)
        
    ScoreMember.objects.bulk_create(score_members)

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    ScoreMember.objects.filter(id=response).delete()

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

    ScoreMember.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

# 工作台展示成员考核评分
def select_workbench(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    rater_id = request.POST.get('id', default=None)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month 

    scores = ScoreMember.objects.filter(rater=rater_id, add_date__year=year, add_date__month=month).values('staff_id')

    for score in scores:
        score['staff_name'] = Staff.objects.filter(id=score['staff_id']).values().first()['name']

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

    scores = ScoreMember.objects.filter(staff=id, add_date__year=year, add_date__month=month).values()

    for score in scores:
        score.pop('add_date')
        score.pop('mod_date')

    data = {}
    data['response'] = list(scores)

    return HttpResponse(json.dumps(data, ensure_ascii=False))