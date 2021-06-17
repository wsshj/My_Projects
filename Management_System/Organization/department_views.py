# from django.shortcuts import render
from datetime import date
from django.http import HttpResponse
import json

from Organization.models import Department

def has_none(values):
    for value in values:
        if value is None:
            return True

    return False

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['name'] = request.get('name', default=None)
    response['level'] = request.get('level', default=0)
    response['describe'] = request.get('describe', default='')

    if has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    department = Department(name=response['name'])
    department = Department(name=response['level'])
    department = Department(name=response['describe'])

    department.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Department.objects.filter(id=response).delete()

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

    Department.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "GET":
        return HttpResponse("<p>请求方式错误！</p>")

    # response = Department.objects.all()
    data = {}

    response = Department.objects.values()

    data['department'] = list(response)

    json_data = json.dumps(data,ensure_ascii=False)

    return HttpResponse(json_data)
