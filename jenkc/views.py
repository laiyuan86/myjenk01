from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from jenkc import jenkfunc


def index(request):
    jobs_dic = jenkfunc.get_jobs()
    build_num = jenkfunc.get_jobs_build_num()
    return render(request, 'jenkc/index.html', {'jobs_dic': jobs_dic, 'build_num': build_num})


def test(request):
    avc=request.GET.get('jobname')
    jobdes = jenkfunc.get_job_detail_info(avc)
    return render(request, 'jenkc/jobinfo.html', {'jobdes': jobdes})


def test01(request):
    build_num = jenkfunc.get_jobs_build_num()
    return render(request, 'jenkc/demo.html', {'build_num': build_num})


def jobs_list(request):
    result = jenkfunc.get_all_data()
    jobdes = result[1]
    return render(request, 'jenkc/jobslist.html', {"jobdes": jobdes})


def get_jobnum_data(request):
    result = jenkfunc.get_all_data()
    jobnum = result[0]
    return  render(request, 'jenkc/index.html', {'jobnum': jobnum})


def get_job_buildinfo(request):
    jobname = request.GET.get('jobname')
    result = jenkfunc.get_job_obj(jobname)
    return render(request, 'jenkc/jobinfo.html', {'jobuild': result, 'jobname': jobname})


def tu_test(request):
    joblist = jenkfunc.get_joblist()
    print(joblist)
    return render(request,"jenkc/test01.html", {'joblist': joblist})


def search(request):
    result = request.GET.getlist('bt')
    if result:
        begintime = result[0]
        endtime = result[1]
    else:
        begintime = "2018-10-23 00:00:00"
        endtime = "2018-10-23 00:00:00"
    print(begintime, endtime)
    jobuild = jenkfunc.search_build_history(begintime, endtime)
    return render(request, "jenkc/index.html", {'jobuild': jobuild})



