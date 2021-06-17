from django.shortcuts import render
from django.http import HttpResponse
import json

from Organization.models import Staff
from Organization.models import Department
from Organization.models import Position

# Create your staff views here.
def has_none(values):
    for value in values:
        if value is None:
            return True

    return False

def select_by_id(staff_id):
    staffs = Staff.objects.filter(id=staff_id).values()

    return staffs

def select_by_number(staff_number):
    staffs = Staff.objects.filter(number=staff_number).values()

    return staffs

def form_json(staffs):
    data = {}    

    for staff in staffs:
        staff['entry_time'] = staff['entry_time'].strftime("%Y-%m-%d")
        staff['department'] = Department.objects.filter(id=staff['department_id']).values('name').first()['name']
        staff['position'] = Position.objects.filter(id=staff['position_id']).values('name').first()['name']
    
    data['staff'] = list(staffs)

    return json.dumps(data,ensure_ascii=False)

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['name'] = request.get('name', default=None)
    response['level'] = request.get('level', default=0)
    response['describe'] = request.get('describe', default='')

    if has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    department = Staff(name=response['name'])
    department = Staff(name=response['level'])
    department = Staff(name=response['describe'])

    department.save()

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Staff.objects.filter(id=response).delete()

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

    Staff.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['id'] = request.POST.get('id', default=None)
    response['number'] = request.POST.get('number', default=None)

    if not response['id'] is None:
        staffs = select_by_id(response['id'])
    elif not response['number'] is None:
        staffs = select_by_number(response['number'])
    else:
        staffs = Staff.objects.values()

    json_data = form_json(staffs)

    return HttpResponse(json_data)

def login(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = {}

    response['number'] = request.POST.get('username', default=None)
    response['password'] = request.POST.get('password', default=None)

    if has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    if Staff.objects.filter(number=response['number']).count() == 0:
        return HttpResponse("<p>用户名错误</p>")

    password = Staff.objects.filter(number=response['number']).values('passwd').first()['passwd']

    if response['password'] == password:
        return HttpResponse(form_json(select_by_number(response['number'])))
    else:
        return HttpResponse("<p>密码错误</p>")
