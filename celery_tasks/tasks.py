from celery import Celery
from django.utils import timezone
import re,os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestAutomation.settings')
django.setup()
from interface_auto.models import InterfaceSuit,InterfaceSuitExecuteRecord
from interface_auto.run_case import RunCase

# app = Celery("celery_tasks.tasks",broker="redis://127.0.0.1:6379/0")
app = Celery('tasks',  backend='redis://localhost:6379/0', broker='redis://localhost:6379/1')


@app.task
def execute_interface_case_suit(suitId,execute_person):
    case_suit = InterfaceSuit.objects.get(id=suitId)
    case_list = case_suit.interfaceCase.all()
    # 获取所有cookie列数据，判断是否存在用例依赖
    runCase = RunCase()
    cookies = []
    for case in case_list:
        cookies.append(case.request_cookie)
    # 如果匹配${test_01}成功，则表示存在依赖
    pattern = '^\$\{(.[^\.]+)\}$'
    cookie_list = []
    match_result = None
    for cookie_depend in cookies:
        if cookie_depend is not None:
            match_result = re.match(pattern, cookie_depend)
        if match_result:
            cookie_list.append(match_result.group(1))
    runCase.cookie_dict = dict.fromkeys(cookie_list, '')
    interfacesuitexecuterecord = InterfaceSuitExecuteRecord()
    interfacesuitexecuterecord.start_time = timezone.now()
    interfacesuitexecuterecord.execute_person = execute_person
    interfacesuitexecuterecord.ececute_status = 2  # 执行中状态
    interfacesuitexecuterecord.interface_suit = case_suit
    interfacesuitexecuterecord.save()
    for case_data in case_list:
        runCase.run_case_by_data(case_data, interfacesuitexecuterecord)
    interfacesuitexecuterecord.end_time = timezone.now()
    interfacesuitexecuterecord.save()

