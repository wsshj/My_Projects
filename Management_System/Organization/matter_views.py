from django.shortcuts import render
from django.http import HttpResponse
import json

from Organization import common

from Organization.models import Matter

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['name'] = request.POST.get('name', default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    department = Matter(
        name=response['name'],
        )

    department.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Matter.objects.filter(id=response).delete()

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

    Matter.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "GET":
        return HttpResponse("<p>请求方式错误！</p>")

    data = {}

    response = Matter.objects.values()

    data['matter'] = list(response)

    return HttpResponse(json.dumps(data, ensure_ascii=False))