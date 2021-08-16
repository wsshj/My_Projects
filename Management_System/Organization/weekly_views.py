from django.shortcuts import render
from django.http import HttpResponse
import json

from Organization import common

from Organization.models import Weekly

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['number'] = request.POST.get('number', default=None)
    response['name'] = request.POST.get('name', default=None)
    response['type'] = request.POST.get('type', default=None)
    response['state'] = request.POST.get('state', default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    department = Weekly(
        number=response['number'],
        name=response['name'],
        type=response['type'],
        state=response['state'],
        )

    department.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Weekly.objects.filter(id=response).delete()

    return HttpResponse("<p>删除成功</p>")

def update(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['id'] = request.get('id', default=None)
    response['key'] = request.get('key', default=None)
    response['value'] = request.get(response['key'], default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    data = {response['key'] : response['value']}

    Weekly.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    pass