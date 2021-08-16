from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime

from Organization import common

from Organization.models import Daily
from Organization.models import Staff
from Organization.models import Task
from Organization.models import Matter
from Organization.models import Project
from Organization.models import Department

def insert(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    daily_list = json.loads(request.POST.get('daily_list', default=None))

    dailies = []

    for daily_item in daily_list:
        response = {}

        response['number'] = daily_item.get('number', None)
        response['name'] = daily_item.get('name', None)
        response['staff'] = daily_item.get('staff', None)
        response['matter'] = daily_item.get('matter', None)
        response['project'] = daily_item.get('project', None)
        response['task'] = daily_item.get('task', None)
        response['time'] = daily_item.get('time', None)
        response['progress'] = daily_item.get('progress', None)
        response['content'] = daily_item.get('content', None)

        if common.has_none(response):
            return HttpResponse("<p>参数错误！</p>")

        daily = Daily(
            number=response['number'],
            name=response['name'],
            staff=Staff.objects.get(id=response['staff']),
            matter=Matter.objects.get(id=response['matter']),
            project=Project.objects.get(id=response['project']),
            task=Task.objects.get(id=response['task']),
            time=response['time'],
            progress=response['progress'],
            content=response['content'],
            )

        dailies.append(daily)
        
    Daily.objects.bulk_create(dailies)

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")

    Daily.objects.filter(id=response).delete()

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

    Daily.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

def select(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    staff_id = request.POST.get('id', default=None)

    if not staff_id is None:
        daily = Daily.objects.filter(staff=staff_id).values()
        json = select_to_json(daily)
    else:
        daily = Daily.objects.values()
        json = select_to_json(daily)

    return HttpResponse(json)

def select_member(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    id = request.POST.get('id', default=None)

    staffs = Staff.objects.filter(bossnumber=id).values()
    member_daily = []
    for staff in staffs:
        dailys = Daily.objects.filter(staff=staff['id']).values()
        data = {}
        for daily in dailys:
            daily['staff_name'] = staff['name']
            daily['matter_name'] = Matter.objects.filter(id=daily['matter_id']).values().first()['name']
            daily['project_name'] = Project.objects.filter(id=daily['project_id']).values().first()['name']
            daily['task_name'] = Task.objects.filter(id=daily['task_id']).values().first()['name']
            daily['add_date'] = daily['add_date'].strftime('%Y-%m-%d %H:%H:%S')
            daily.pop('mod_date')
        
        data[staff['name']] = list(dailys)
        member_daily.append(data)

    return HttpResponse(json.dumps(member_daily, ensure_ascii=False))

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

    dailies = Daily.objects.filter(staff=id, add_date__year=year, add_date__month=month).values()

    for daily in dailies:
        matter = Matter.objects.filter(id=daily['matter_id']).values().first()
        daily['matter_name'] = matter['name']
        project = Project.objects.filter(id=daily['project_id']).values().first()
        daily['project_number'] = project['number']
        daily['project_name'] = project['name']
        daily['project_type'] = project['type']
        task = Task.objects.filter(id=daily['task_id']).values().first()
        daily['task_name'] = task['name']
        daily['task_progress'] = task['progress']
        daily['date'] = daily['add_date'].strftime('%Y-%m-%d')
        daily.pop('add_date')
        daily.pop('mod_date')
        
    data = {}
    data['response'] = form_data(list(dailies))

    return HttpResponse(json.dumps(data, ensure_ascii=False))

def select_daily(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    id = request.POST.get('id', default=None)
    date = request.POST.get('date', default=None)

    if date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    start_date = end_date + datetime.timedelta(days=-7)

    dailies = Daily.objects.filter(staff=id, add_date__range=(start_date, end_date)).values()

    for daily in dailies:
        matter = Matter.objects.filter(id=daily['matter_id']).values().first()
        daily['matter_name'] = matter['name']
        project = Project.objects.filter(id=daily['project_id']).values().first()
        daily['project_number'] = project['number']
        daily['project_name'] = project['name']
        daily['project_type'] = project['type']
        task = Task.objects.filter(id=daily['task_id']).values().first()
        daily['task_name'] = task['name']
        daily['task_progress'] = task['progress']
        daily['date'] = daily['add_date'].strftime('%Y-%m-%d')
        daily.pop('add_date')
        daily.pop('mod_date')
        
    data = {}
    data['response'] = form_data(list(dailies))

    return HttpResponse(json.dumps(data, ensure_ascii=False))

def search_daily(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    id = request.POST.get('id', default=None)
    date = request.POST.get('date', default=None)

    if date is None:
        search_date = datetime.datetime.now()
    else:
        search_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    dailies = Daily.objects.filter(staff=id, add_date__date=search_date).values()

    for daily in dailies:
        matter = Matter.objects.filter(id=daily['matter_id']).values().first()
        daily['matter_name'] = matter['name']
        project = Project.objects.filter(id=daily['project_id']).values().first()
        daily['project_number'] = project['number']
        daily['project_name'] = project['name']
        daily['project_type'] = project['type']
        task = Task.objects.filter(id=daily['task_id']).values().first()
        daily['task_name'] = task['name']
        daily['task_progress'] = task['progress']
        daily['date'] = daily['add_date'].strftime('%Y-%m-%d')
        daily.pop('add_date')
        daily.pop('mod_date')
        
    data = {}
    data['response'] = form_data(list(dailies))

    return HttpResponse(json.dumps(data, ensure_ascii=False))

def state_daily(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    date = request.POST.get('date', default=None)

    if date is None:
        search_date = datetime.datetime.now()
    else:
        search_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    staffs = Staff.objects.values('id','name','department_id')

    dailies = Daily.objects.filter(add_date__date=search_date).values('staff_id').distinct()

    finish = []

    for daily in dailies:
        finish.append(daily['staff_id'])

    for staff in staffs:
        department = Department.objects.filter(id=staff['department_id']).values().first()
        staff['department_name'] = department['name']
        if staff['id'] in finish:
            staff['state'] = 1
        else:
            staff['state'] = 0

    data = {}
    data['response'] = list(staffs)

    return HttpResponse(json.dumps(data, ensure_ascii=False))

def task_fun(datas):
    responses = []
    task_list = []

    for data in datas:
        if task_list == []:
            task_list.append(data['task_id'])
        else:
            if not data['task_id'] in task_list:
                task_list.append(data['task_id'])
    
    for task_id in task_list:
        task_dict = {}
        task_dict['task_id'] = task_id
        task_dict['task_name'] = ''
        task_dict['task_progress'] = 0
        task_dict['task_time'] = 0
        task_dict['value'] = []
        for data in datas:
            if data['task_id'] == task_id:
                task_dict['task_name'] = data['task_name']
                task_dict['task_progress'] = data['task_progress']
                task_dict['task_time'] += data['time']

                daily_dict = {}
                daily_dict['daily_id'] = data['id']
                daily_dict['daily_name'] = data['name']
                daily_dict['daily_time'] = data['time']
                daily_dict['daily_progress'] = data['progress']
                daily_dict['daily_content'] = data['content']

                task_dict['value'].append(daily_dict)

        responses.append(task_dict)
        
    return responses
    
def project_fun(datas):
    responses = []
    project_list = []

    for data in datas:
        if project_list == []:
            project_list.append(data['project_id'])
        else:
            if not data['project_id'] in project_list:
                project_list.append(data['project_id'])
    
    for project_id in project_list:
        project_dict = {}
        project_dict['project_id'] = project_id
        project_dict['project_name'] = ''
        project_dict['project_type'] = ''
        project_dict['value'] = []
        for data in datas:
            if data['project_id'] == project_id:
                project_dict['project_name'] = data['project_name']
                project_dict['project_type'] = data['project_type']
                project_dict['value'].append(data)

        responses.append(project_dict)
    
    for response in responses:
        response['value'] = task_fun(response['value'])

    return responses

def form_data(datas):
    responses = []
    date_list = []

    for data in datas:
        if date_list == []:
            date_list.append(data['date'])
        else:
            if not data['date'] in date_list:
                date_list.append(data['date'])

    for date in date_list:
        date_dict = {}
        date_dict['date'] = date
        date_dict['value'] = []
        for data in datas:
            if data['date'] == date:
                date_dict['value'].append(data)

        responses.append(date_dict)

    for response in responses:
        response['value'] = project_fun(response['value'])

    return responses
