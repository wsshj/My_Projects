from django.shortcuts import render
from django.http import HttpResponse
import json

from Organization.models import Project
from Organization.models import Staff

def has_none(values):
    for value in values:
        if value is None:
            return True

    return False

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['number'] = request.POST.get('number', default=None)
    response['name'] = request.POST.get('name', default=None)
    response['director'] = request.POST.get('director', default=None)
    response['manager'] = request.POST.get('manager', default=None)
    response['type'] = request.POST.get('type', default=None)
    response['state'] = request.POST.get('state', default=None)
    response['begin_time'] = request.POST.get('begin_time', default=None)
    response['delivery_time'] = request.POST.get('delivery_time', default=None)
    response['state_description'] = request.POST.get('state_description', default='')
    response['project_description'] = request.POST.get('project_description', default='')
    response['member'] = request.POST.get('member', default=None)

    if has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    department = Project(
        number=response['number'],
        name=response['name'],
        director=response['director'],
        manager=response['manager'],
        type=response['type'],
        state=response['state'],
        begin_time=response['begin_time'],
        delivery_time=response['delivery_time'],
        state_description=response['state_description'],
        project_description=response['project_description'],
        member=response['member'],
        )

    department.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Project.objects.filter(id=response).delete()

    return HttpResponse("<p>删除成功</p>")

def update(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['id'] = request.get('id', default=None)
    response['key'] = request.get('key', default=None)
    response['value'] = request.get(response['key'], default=None)

    if has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    data = {response['key'] : response['value']}

    Project.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "GET":
        return HttpResponse("<p>请求方式错误！</p>")

    data = {}

    response = Project.objects.values()

    data['position'] = list(response)

    json_data = json.dumps(data,ensure_ascii=False)

    return HttpResponse(json_data)
