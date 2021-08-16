from django.shortcuts import render
from django.http import HttpResponse
import json

from Organization import common

from Organization.models import Task
from Organization.models import Matter
from Organization.models import Project
from Organization.models import Staff
from Organization.models import Daily

def select_to_json(responses):
    data = {}

    for response in responses:
        response['project_number'] = Project.objects.filter(id=response['project_id']).values().first()['number']
        response['project_name'] = Project.objects.filter(id=response['project_id']).values().first()['name']
        response['project_state'] = Project.objects.filter(id=response['project_id']).values().first()['state']
        response.pop('add_date')
        response.pop('mod_date')

    data['response'] = list(responses)

    return json.dumps(data, ensure_ascii=False)

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['number'] = request.POST.get('number', default=None)
    response['name'] = request.POST.get('name', default=None)
    response['staff'] = request.POST.get('staff', default=None)
    response['matter'] = request.POST.get('matter', default=None)
    response['project'] = request.POST.get('project', default=None)
    response['state'] = request.POST.get('state', default=None)
    response['progress'] = request.POST.get('progress', default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    task = Task(
        number=response['number'],
        name=response['name'],
        staff=Staff.objects.get(id=response['staff']),
        matter=Matter.objects.get(id=response['matter']),
        project=Project.objects.get(id=response['project']),
        state=response['state'],
        progress=response['progress'],
        )

    task.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Task.objects.filter(id=response).delete()

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

    Task.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    staff_id = request.POST.get('id', default=None)
    project_id = request.POST.get('project_id', default=None)

    tasks = Task.objects.filter(staff=staff_id,project=project_id).values()

    json = select_to_json(tasks)

    return HttpResponse(json)

def select_daily(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    id = request.POST.get('id', default=None)
    date = request.POST.get('date', default=None)

    tasks = Task.objects.filter(staff=id).values()

    for task in tasks:
        task['matter_name'] = Matter.objects.filter(id=task['matter_id']).values().first()['name']
        task['project_number'] = Project.objects.filter(id=task['project_id']).values().first()['number']
        task['project_name'] = Project.objects.filter(id=task['project_id']).values().first()['name']
        task['project_state'] = Project.objects.filter(id=task['project_id']).values().first()['state']
        dailys = Daily.objects.filter(task=task['id'], staff=id).values()
        for daily in dailys:
            daily.pop('add_date')
            daily.pop('mod_date')
        task['daily'] = list(dailys)
        task.pop('add_date')
        task.pop('mod_date')
        
    data = {}
    data['response'] = list(tasks)

    return HttpResponse(json.dumps(data, ensure_ascii=False))
