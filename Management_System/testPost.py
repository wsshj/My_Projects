import requests
import json
# GET 请求
# 部门
department_url = "http://localhost:8000/department/select/"
# 职位
position_url = "http://localhost:8000/position/select/"
# 事项
matter_url = "http://localhost:8000/matter/select/"

# POST 请求
# 登录
url_1 = "http://localhost:8000/login/"
data_1 = {"username":"BF80029", "password":"123456"}

# 项目
project_url_1 = "http://localhost:8000/project/insert/"
project_data_1= {
    "number":"BFXSY-PM-HD-2021-001", "name":"“融汇智通—2021”城市突发事件情景认知技术挑战赛",
    "matter":"1", "director":1, "manager":7,
    "type":"互动", "state":"正在进行",
    "begin_time":"2021-03-02", "delivery_time":"2030-03-02",
    "state_description":"正常", "project_description":"正常",
    "member": "[3,4,5]"
    }

project_url_2 = "http://localhost:8000/project/update/"
project_data_2 = {
    "id":"3",
    "key":"number",
    "value":"BF80108"
    }

project_url_3 = "http://localhost:8000/project/delete/"
project_data_3 = {
    "id":"3",
    }

project_url_41 = "http://localhost:8000/project/select/"
project_data_41 = {
    "id":"1"
    }

project_url_42 = "http://localhost:8000/project/select/matter/"
project_data_42 = {
    "id":"1",
    "staff_id":"38"
    }

project_url_43 = "http://localhost:8000/project/select/memberhours/"
project_data_43 = {
    "id":"1"
    }
    

# 日报
daily_url_1 = "http://localhost:8000/daily/insert/"
daily_data_1 = {
    "daily_list":json.dumps([{"number":"DY00001", "name":"上课",
    "staff":38, "matter":1, "project":2, "task":1,
    "time":"8", "progress":50,
    "content":"讲Qt"},
    {"number":"DY00002", "name":"上课la",
    "staff":38, "matter":1, "project":2, "task":1,
    "time":"8", "progress":50,
    "content":"讲Qt"}
    ])
    }

daily_url_2 = "http://localhost:8000/daily/update/"
daily_data_2 = {
    "id":"38",
    "key":"number",
    "value":"BF80108"
    }

daily_url_3 = "http://localhost:8000/daily/delete/"
daily_data_3 = {
    "id":"3",
    }

daily_url_41 = "http://localhost:8000/daily/select/self/"
daily_data_41 = {
    "id":"38",
    # "number":"BF80108"
    }

daily_url_42 = "http://localhost:8000/daily/select/member/"
daily_data_42 = {
    "id":"38",
    # "number":"BF80108"
    }

# 人员
staff_url_1 = "http://localhost:8000/staff/insert/"
staff_data_1 = {
    "number":"BF80108",
    "name":"双捷",
    "sex":"男",
    "department_id":2,
    "position_id":3,
    "boss_id":1,
    "boss_name":"于宝华",
    "entry_time":"2021-03-17",
    "phone":"13623622322"
    }

staff_url_2 = "http://localhost:8000/staff/update/"
staff_data_2 = {
    "id":"38",
    "key":"number",
    "value":"BF80108"
    }

staff_url_3 = "http://localhost:8000/staff/delete/"
staff_data_3 = {
    "id":"98",
    }

staff_url_4 = "http://localhost:8000/staff/select/"
staff_data_4 = {
    # "id":"1",
    # "number":"BF80108"
    }

# 任务
task_url_1 = "http://localhost:8000/task/insert/"
task_data_1 = {
    "number":"TK00001", "name":"任务","staff":38,
    "matter":1, "project":1,
    "state":"正常", "progress":"50",
    }

task_url_2 = "http://localhost:8000/task/update/"
task_data_2 = {
    "id":"38",
    "key":"number",
    "value":"BF80108"
    }

task_url_3 = "http://localhost:8000/task/delete/"
task_data_3 = {
    "id":"3",
    }


task_url_41 = "http://localhost:8000/task/select/"
task_data_41 = {
    "id":"38",
    "project_id":1
    }

task_url_42 = "http://localhost:8000/task/select/daily/"
task_data_42 = {
    "id":"38"
    }

# 绩效
score_url_1 = "http://localhost:8000/score/insert/"
score_data_1 = {
    "score_table": json.dumps([
        {"project":1,"staff":38, "rater":1,"project_weight":30,"score_weight":50,"score":0,"date":"2021-06-30"},
        {"project":1,"staff":38,"rater":28, "project_weight":30,"score_weight":30,"score":0,"date":"2021-06-30"}
    ])
}

score_url_2 = "http://localhost:8000/score/update/"
score_data_2 = {
    "id":"2",
    "key":"number",
    "value":"BF80108"
    }

score_url_3 = "http://localhost:8000/score/delete/"
score_data_3 = {
    "id":"3",
    }

score_url_4 = "http://localhost:8000/score/select/"
score_data_4 = {
	"staff_id": "38",
	"project_id": "1"
}

# 日报查看
daily_select_url = "http://localhost:8000/daily/select/"
daily_select_data = {
    "id": "38",
	"date": "2021-07-05"
}

# 日报查询
daily_search_url = "http://localhost:8000/daily/search/"
daily_search_data = {
    "id": "38",
	"date": "2021-07-01"
}

# 日报状态
daily_state_url = "http://localhost:8000/daily/state/"
daily_state_data = {
	"date": "2021-06-29"
}

# 日报月度统计
daily_monthly_select_url = "http://localhost:8000/daily/select/monthly/"
daily_monthly_select_data = {
	"id": "38",
	"date": "2021-06-01"
}

# 绩效月度统计
score_monthly_select_url = "http://localhost:8000/monthly/select/daily/"
score_monthly_select_data = {
	"id": "38",
	"date": "2021-06-01"
}

# 工作台展示
score_workbench_select_url = "http://localhost:8000/score/select/workbench/"
score_workbench_select_data = {
	"id": "28",
}

# 项目考核展示
score_project_select_url = "http://localhost:8000/score/select/project/"
score_project_select_data = {
	"id": "2"
}

# 项目考核打分
score_url_2 = "http://localhost:8000/score/update/"
score_data_2 = {
    "id":"2",
    "key":"score",
    "value":"20"
    }


res = requests.post(url=project_url_43,data=project_data_43)
print(res.text)

# import datetime

# date = '2020-09-07'

# year = datetime.datetime.strptime(date, "%Y-%m-%d").year
# month = datetime.datetime.strptime(date, "%Y-%m-%d").month

# print(year)
# print(month)

