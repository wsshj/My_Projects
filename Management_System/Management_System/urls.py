"""Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Organization import department_views
from Organization import position_views
from Organization import staff_views
from Organization import task_views
from Organization import matter_views
from Organization import project_views
from Organization import daily_views
from Organization import score_views
from Organization import monthly_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', staff_views.login),

    path('department/insert/', department_views.insert),
    path('department/delete/', department_views.delete),
    path('department/update/', department_views.update),
    path('department/select/', department_views.select),

    path('position/insert/', position_views.insert),
    path('position/delete/', position_views.delete),
    path('position/update/', position_views.update),
    path('position/select/', position_views.select),

    path('staff/insert/', staff_views.insert),
    path('staff/delete/', staff_views.delete),
    path('staff/update/', staff_views.update),
    path('staff/select/', staff_views.select),

    path('project/insert/', project_views.insert),
    path('project/delete/', project_views.delete),
    path('project/update/', project_views.update),
    path('project/select/', project_views.select),
    path('project/select/matter/', project_views.select_matter),
    path('project/select/memberhours/', project_views.select_member_hours),

    path('task/insert/', task_views.insert),
    path('task/delete/', task_views.delete),
    path('task/update/', task_views.update),
    path('task/select/', task_views.select),
    path('task/select/daily/', task_views.select_daily),

    path('matter/insert/', matter_views.insert),
    path('matter/delete/', matter_views.delete),
    path('matter/update/', matter_views.update),
    path('matter/select/', matter_views.select),

    path('score/insert/', score_views.insert),
    path('score/delete/', score_views.delete),
    path('score/update/', score_views.update),
    path('score/select/project/', score_views.select_project),
    path('score/select/workbench/', score_views.select_workbench),
    path('score/select/monthly/', score_views.select_monthly),

    path('daily/insert/', daily_views.insert),
    path('daily/delete/', daily_views.delete),
    path('daily/update/', daily_views.update),
    path('daily/select/', daily_views.select_daily),
    path('daily/search/', daily_views.search_daily),
    path('daily/state/', daily_views.state_daily),
    path('daily/select/monthly/', daily_views.select_monthly),
]
