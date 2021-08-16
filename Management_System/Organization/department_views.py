# from django.shortcuts import render
from datetime import date
from django.http import HttpResponse
import json

from Organization import common
from Organization.models import Department

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['name'] = request.get('name', default=None)
    response['pid'] = request.get('pid', default=None)
    response['describe'] = request.get('describe', default='')

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    department = Department(name=response['name'])
    department = Department(name=response['pid'])
    department = Department(name=response['describe'])

    department.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Department.objects.filter(id=response).delete()

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
