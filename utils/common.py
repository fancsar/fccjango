# -*- coding: utf-8 -*-
# @Time   :2020/6/4 21:50
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :common.py
import yaml
import json
import os

from httprunner.task import HttpRunner
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from reports.models import Reports


def generate_testcase_files(instance, env, testcase_dir_path):
    """
    @param instance:  传用例对象，获取用例请求
    @param env:  传环境变量对象
    @param testcase_dir_path: 传文件夹路径
    @return:
    """
    testcases_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ' '
            }
        }
    }
    testcases_list.append(config)
    # 前置参数转换为字典
    include = json.loads(instance.include, encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(instance.request, encoding='utf-8')
    # 获取接口名称
    interface_name = instance.interface.name
    # 获取项目名称
    project_name = instance.interface.project.name

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    # 创建项目名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = DebugTalks.objects.get(project__name=project_name)
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ' '
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), mode='w', encoding='utf-8') as file:
            file.write(debugtalk)
    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    # 在项目目录下创建接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # 将testcases_list中的config进行替换
    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request.get('config').get('request').setdefault('base_url', env.base_url)
            config_request['config']['name'] = instance.name
            # 将list中config,进行替换，考虑到include中‘config’为空时，会报错
            testcases_list[0] = config_request

    # 若include前置中有testcases,那么添加到testcases_list中
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcases_obj = Testcases.objects.get(id=t_id)
            if testcases_obj:
                testcase_request = json.loads(testcases_obj.request, encoding='utf-8')
                testcases_list.append(testcase_request)

    # 将当前用例的request添加到testcases_list中
    testcases_list.append(request)

    # allow_unicode = True  处理中文乱码问题
    with open(os.path.join(testcase_dir_path, instance.name + '.yml'), mode='w', encoding='utf-8') as file:
        yaml.dump(testcases_list, file, allow_unicode=True)


def run_testcase(instance, testcase_dir_path):
    runner = HttpRunner()
    runner.run(testcase_dir_path)
    # runner.summary 统计了用例运行详情
    runner.summary = timestamp_to_datetime(runner.summary, type=False)

    try:
        # 报告名称为用例名称
        report_name = instance.name
    except Exception as e:  # 如果报告名称不存在:
        report_name = '被遗弃的报告' + '-' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
    # create_report生成报告，返回报告id值
    report_id = create_report(runner, report_name=report_name)
    data_dict = {
        "id": report_id
    }

    return Response(data_dict, status=status.HTTP_201_CREATED)


# 将summary中的时间戳进行格式化
def timestamp_to_datetime(summary, type=True):
    if not type:
        time_stamp = int(summary['time']['start_at'])
        # 对开始时间戳进行转换，并重新赋值给start_datetime
        summary['time']['start_datetime'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = datetime.fromtimestamp(time_stamp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary


# 创建报告
def create_report(runner, report_name=None):
    time_stamp = int(runner.summary['time']['start_at'])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime

    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                # 字节内容展示时，前端报错，所以进行转换，通过decode('utf-8')进行解码
                record['meta_data']['response']['content'] = record['meta_data']['response']['content'].decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue
    # 对summary进行json转换(字节转换时，dumps会报错，所以要进行转换)
    summary = json.dumps(runner.summary, ensure_ascii=False)
    # 报告名称生成
    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    # 生成报告，会返回报告生成的路径
    report_path = runner.gen_html_report(html_report_name=report_name)
    # 报告数据库需要html源码
    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),  # 用例运行成功数
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    # 返回报告id,前端设置的功能，需要传递id值
    return report_obj.id
