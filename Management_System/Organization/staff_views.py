from django.shortcuts import render
from django.http import HttpResponse
# from django.core import serializers
import json

from Organization import common

from Organization.models import Staff
from Organization.models import Department
from Organization.models import Position

def select_to_json(responses):
    data = {}
    data['status'] = 200

    for response in responses:
        response['entry_time'] = response['entry_time'].strftime('%Y-%m-%d')
        response['department_name'] = Department.objects.filter(id=response['department_id']).values().first()['name']
        response['position_name'] = Position.objects.filter(id=response['position_id']).values().first()['name']
        response.pop('add_date')
        response.pop('mod_date')
    
    data['response'] = list(responses)

    return json.dumps(data,ensure_ascii=False)

# Create your staff views here.
def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['number'] = request.POST.get('number', default=None)
    response['name'] = request.POST.get('name', default=None)
    response['sex'] = request.POST.get('sex', default=None)
    response['department_id'] = request.POST.get('department_id', default=None)
    response['position_id'] = request.POST.get('position_id', default=None)
    response['boss_id'] = request.POST.get('boss_id', default=None)
    response['boss_name'] = request.POST.get('boss_name', default=None)
    response['entry_time'] = request.POST.get('entry_time', default=None)
    response['phone'] = request.POST.get('phone', default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    staff = Staff(
        number=response['number'],
        name=response['name'],
        department=Department.objects.get(id=response['department_id']),
        position=Position.objects.get(id=response['position_id']),
        sex=response['sex'],
        boss_id=response['boss_id'],
        boss_name=response['boss_name'],
        entry_time=response['entry_time'],
        phone=response['phone'],
        )

    staff.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Staff.objects.filter(id=response).delete()

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

    Staff.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['id'] = request.POST.get('id', default=None)
    response['number'] = request.POST.get('number', default=None)

    if not response['id'] is None:
        staffs = Staff.objects.filter(id=response['id']).values().order_by('id')
    elif not response['number'] is None:
        staffs = Staff.objects.filter(number=response['number']).values().order_by('id')
    else:
        staffs = Staff.objects.values().order_by('id')

    json = select_to_json(staffs)

    return HttpResponse(json)

def login(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['number'] = request.POST.get('username', default=None)
    response['password'] = request.POST.get('password', default=None)

    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    if Staff.objects.filter(number=response['number']).count() == 0:
        return HttpResponse("<p>用户名错误</p>")

    password = Staff.objects.filter(number=response['number']).values('passwd').first()['passwd']

    if response['password'] == password:
        # staff = Staff.objects.filter(number=response['number']).select_related()
        # print(staff.query.__str__())

        staff_json = select_to_json(Staff.objects.filter(number=response['number']).values())

        return HttpResponse(staff_json)
    else:
        return HttpResponse("<p>密码错误</p>")
