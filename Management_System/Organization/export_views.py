from django.shortcuts import render
from django.http import Http404, FileResponse

import os

from Organization.models import Daily
from Organization.models import Project
from Organization.models import Task

# Create your views here.
def select_daily(request):
    if request.method != "POST":
        return HttpResponse("<p>请求方式错误！</p>")

    id = request.POST.get('id', default=None)
    date = request.POST.get('date', default=None)

    if date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    end_date = end_date + datetime.timedelta(days=1)
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


def vacancyRateReport(request):
    path = os.path.dirname(os.path.dirname(__file__))
    filePath = '%s\\file\\vacancy-rate-report.docx' % path

    try:
        response = FileResponse(open(filePath, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filePath)

        return response
    except Exception:
        raise Http404


def completionReport(request):
    date = request.GET.get('date', MaxDate('line_abnormal_info'))
    createReport(date)

    path = os.path.dirname(os.path.dirname(__file__))
    filePath = '%s\\file\\completion-report.docx' % path

    try:
        response = FileResponse(open(filePath, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + 'completion-report-%s.docx' % date

        return response
    except Exception:
        raise Http404
