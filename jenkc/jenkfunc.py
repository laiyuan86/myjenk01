#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author = "laiyuan"
# Date: 2018/11/08

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import  Build
from jenkc.dbhelp import sqlfunc
import pytz, datetime
import time


#获取服务实例函数
def get_server_instance():
    jenkins_url = "http://172.16.21.21:8080/"
    server = Jenkins(jenkins_url, username='admin', password="8Q3K3m3AEy")
    return server


def get_jobs():
    server = get_server_instance()
    jobs = server.get_jobs()
    jobs_dic = {}
    for job_name, job_instance in jobs:
        jobs_dic[job_name] = job_instance.get_description()
    return jobs_dic


def get_jobs_build_num():
    server = get_server_instance()
    jobs_list = server.get_jobs_list()
    build_num = {}
    for i in jobs_list:
        try:
            build_num[i] = server[i].get_last_good_buildnumber()
        except:
            pass
    return build_num


def update_db():
    server = get_server_instance()
    jobs = server.get_jobs()
    jobs_info = []
    for job_name, job_instance in jobs:
        jobs_temp = []
        jobs_desc = job_instance.get_description()
        try:
            build_num = server[job_name].get_last_good_buildnumber()
        except:
            pass
        jobs_temp.append(job_name)
        jobs_temp.append(jobs_desc)
        jobs_temp.append(build_num)
        jobs_info.append(jobs_temp)
    print(jobs_info)
    for jobinfo in jobs_info:
        sqlfunc.insert_data(jobinfo[0], jobinfo[1], int(jobinfo[2]))


#获取数据库里job的名字，描述，成功次数。
def get_all_data():
    results = sqlfunc.get_all_data()
    jobnum = {}
    jobdesc = {}
    for job in results:
        jobnum[job[1]] = job[3]
        jobdesc[job[1]] = job[2]
    jobinfo = []
    jobinfo.append(jobnum)
    jobinfo.append(jobdesc)
    return jobinfo


def get_job_detail_info(jobname):
    server = get_server_instance()
    try:
        job_detail_info = server[jobname].get_description()
    except:
        pass
    return job_detail_info


def get_job_obj(jobname):
    server = get_server_instance()
    job = server[jobname]
#    url = job.__dict__['_data']['lastBuild']['url']
#    number = job.__dict__['_data']['lastBuild']['number']
#    obj = Build('http://172.16.21.21:8080/job/file-task-new/25/', 25, job)
    dic = job.__dict__
    dicd = dic['_data']
    dicdb = dicd['builds']
#    print(job)
    job_build_info = []
#    job_build_info.append(job)
    for i in dicdb:
        job_build_dic = {}
#        print(i['url'], i['number'], job)
        lll = Build(i['url'], i['number'], job)
        lll_dic = lll.get_data(i['url']+'api/python/')
        timest = lll_dic['timestamp']/1000
        job_build_dic['发布时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timest))
        job_build_dic['执行结果'] = lll_dic['result']
        job_build_dic['发布次数'] = lll_dic['number']
        job_build_info.append(job_build_dic)

    print(job_build_info)
    return job_build_info
#        for k, v in lll_dic.items():
#            print(k, v)
#        print(timest, lll_dic['number'], lll_dic['result'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timest)))


def updata_jobname_des():
    server = get_server_instance()
    jobs = server.get_jobs()
    jobs_info = []
    for job_name, job_instance in jobs:
        jobs_temp = []
        jobs_desc = job_instance.get_description()
        jobs_temp.append(job_name)
        jobs_temp.append(jobs_desc)
        jobs_info.append(jobs_temp)
#    print(jobs_info)
    for jobs in jobs_info:
        sqlfunc.insert_jobnamedes(jobs[0], jobs[1])


def get_job_buildhistory(jobname):
    server = get_server_instance()
    job = server[jobname]
    dic = job.__dict__
    dicd = dic['_data']
    dicdb = dicd['builds']
    job_build_info = []
    for i in dicdb:
        job_build_dic = {}
        lll = Build(i['url'], i['number'], job)
        lll_dic = lll.get_data(i['url']+'api/python/')
        timest = lll_dic['timestamp']/1000
        job_build_dic['buildtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timest))
        job_build_dic['status'] = lll_dic['result']
        job_build_dic['buildnum'] = lll_dic['number']
        job_build_info.append(job_build_dic)
    for jobbuild in job_build_info:
        sqlfunc.insert_build_history(jobname, jobbuild['buildtime'], jobbuild['buildnum'], jobbuild['status'])
    return job_build_info


#更新数据到数据库
def update_build_history():
    server = get_server_instance()
    jobs_list = server.get_jobs_list()
    for job in jobs_list:
        get_job_buildhistory(job)


def get_joblist():
    result = sqlfunc.get_all_data()
    joblist = []
    for i in result:
        joblist.append(i[1])

    return joblist


def search_build_history(bt, et):
    result = sqlfunc.get_data_fromhistory(bt, et)
    return result


if __name__ == '__main__':
    update_build_history()