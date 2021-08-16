from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum
import json

from Organization import common

from Organization.models import Matter
from Organization.models import Project
from Organization.models import ProjectMember
from Organization.models import Staff
from Organization.models import Daily

def select_to_json(responses):
    data = {}

    for response in responses:
        response['matter_name'] = Matter.objects.filter(id=response['matter_id']).values().first()['name']
        response['director_name'] = Staff.objects.filter(id=response['director_id']).values().first()['name']
        response['manager_name'] = Staff.objects.filter(id=response['manager_id']).values().first()['name']
        response['begin_time'] = response['begin_time'].strftime('%Y-%m-%d')
        response['delivery_time'] = response['delivery_time'].strftime('%Y-%m-%d')
        response['add_date'] = response['add_date'].strftime('%Y-%m-%d %H:%H:%S')
        response.pop('mod_date')

    data['response'] = list(responses)

    return json.dumps(data, ensure_ascii=False)

def select_info_to_json(responses):
    data = {}

    for response in responses:
        response['director_name'] = Staff.objects.filter(id=response['director_id']).values().first()['name']
        response['manager_name'] = Staff.objects.filter(id=response['manager_id']).values().first()['name']
        response['begin_time'] = response['begin_time'].strftime('%Y-%m-%d')
        response['delivery_time'] = response['delivery_time'].strftime('%Y-%m-%d')

        member_list = []
        members = ProjectMember.objects.filter(project=response['id']).values()
        for member in members:   
            member_dict = {}
            member_dict['id'] = member
            member_dict['name'] = Staff.objects.filter(id=member).values().first()['name']
            member_list.append(member_dict)
        response['member'] = member_list

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
    response['matter'] = request.POST.get('matter', default=None)
    response['director'] = request.POST.get('director', default='')
    response['manager'] = request.POST.get('manager', default='')
    response['type'] = request.POST.get('type', default='')
    response['state'] = request.POST.get('state', default=None)
    response['begin_time'] = request.POST.get('begin_time', default='')
    response['delivery_time'] = request.POST.get('delivery_time', default='')
    response['state_description'] = request.POST.get('state_description', default='')
    response['project_description'] = request.POST.get('project_description', default='')
    response['member'] = json.loads(request.POST.get('member', default=None))
    
    if common.has_none(response):
        return HttpResponse("<p>参数错误！</p>")

    project = Project(
        number=response['number'],
        name=response['name'],
        matter=Matter.objects.get(id=response['matter']),
        director=Staff.objects.get(id=response['director']),
        manager=Staff.objects.get(id=response['manager']),
        type=response['type'],
        state=response['state'],
        begin_time=response['begin_time'],
        delivery_time=response['delivery_time'],
        state_description=response['state_description'],
        project_description=response['project_description'],
        )

    project.save()

    project_id = Project.objects.filter(number=response['number']).values('id').last()['id']

    members = []
    for staff_id in response['member']:
        
        member = ProjectMember(
            staff=Staff.objects.get(id=staff_id),
            project=Project.objects.get(id=project_id),
        )

        members.append(member)

    ProjectMember.objects.bulk_create(members)

    return HttpResponse("<p>数据添加成功！</p>")

def delete(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    response = request.POST.get('id', default=None)

    if response is None:
        return HttpResponse("<p>ID为空！</p>")
        
    project_members = ProjectMember.objects.filter(project=response).values()

    Project.objects.filter(id=response).delete()

    for project_member in project_members:
        ProjectMember.objects.filter(id=project_member['id']).delete()

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

    Project.objects.filter(id=response['id']).update(**data)

    return HttpResponse("<p>修改成功</p>")

# 项目明细
def select(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    project_id = request.POST.get('project_id', default=None)
    matter_id = request.POST.get('matter_id', default=None)

    if not project_id is None:
        project = Project.objects.filter(id=project_id).values().order_by('id')
        json = select_info_to_json(project)
    elif not matter_id is None:
        project = Project.objects.filter(matter=matter_id).values().order_by('id')
        json = select_to_json(project)
    else:
        project = Project.objects.values().order_by('id')
        json = select_to_json(project)

    return HttpResponse(json)

# 项目成员工作时长
def select_member_hours(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    project_id = request.POST.get('id', default=None)

    member_ids = ProjectMember.objects.filter(project=project_id).values('staff_id')
    
    members = []
    for member_id in member_ids:
        member = {}
        member['id'] = member_id['staff_id']
        member['name'] = Staff.objects.filter(id=member['id']).values('name').first()['name']
        member['total_time'] = Daily.objects.filter(staff=member['id'],project=project_id).values('time').annotate(total_time=Sum('time'))
        
        if list(member['total_time']) == []:
            member['total_time'] = 0
        else:
            member['total_time'] = list(member['total_time'])[0]['total_time']
        
        members.append(member)

    data = {}
    data['response'] = list(members)

    return HttpResponse(json.dumps(data, ensure_ascii=False))

# 根据事项和员工ID展示项目
def select_matter(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    matter_id = request.POST.get('id', default=None)
    staff_id = request.POST.get('staff_id', default=None)

    if matter_id is None or staff_id is None:
        return HttpResponse("<p>参数错误！</p>")

    ids = []
    projects = []
    
    for id in Project.objects.filter(Q(director=staff_id)|Q(manager=staff_id)).values('id'):
        ids.append(id['id'])
    for id in ProjectMember.objects.filter(staff=staff_id).values('project_id'):
        ids.append(id['project_id'])

    for project in Project.objects.filter(matter=matter_id).values('id','number','name'):
        if project['id'] in ids:
            projects.append(project)

    data = {}
    data['response'] = projects

    return HttpResponse(json.dumps(data, ensure_ascii=False))
