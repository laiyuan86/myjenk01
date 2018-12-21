#!/usr/bin/env python3

import pymysql
import time, datetime
from jenkc.dbhelp import config


#获取数据库信息
def get_db_info():
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print(data)
    db.close()


#插入数据jobname 描述 和buildnum
def insert_data(jobname, jobsecs, buildnum):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO JOBASEINFO(JOBNAME, DESCS, BUILDNUM) VALUES ('%s', '%s', '%d')" % (jobname, jobsecs, buildnum))
        db.commit()
    except:
        db.rollback()
    db.close()


#插入数据 jobname和描述
def insert_jobnamedes(jobname, jobsecs):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        if not select_jobname(jobname):
            cursor.execute("INSERT INTO jenkc_jobsnamedes(jobname, jobdesc) VALUES ('%s', '%s')" % (jobname, jobsecs))
            db.commit()
        else:
            print("%s 已经存在" % jobname)
    except:
        db.rollback()
    db.close()


#查询jobname是否存在
def select_jobname(jobname):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM jenkc_jobsnamedes WHERE jobname = '%s'" % jobname)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return False
    except:
        pass
    db.close()


#查询外键id和buildnum是否存在
def select_num(id, buildnum):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT jobname_id, buildnum FROM jenkc_buildhistory \
        WHERE jobname_id = '%d' AND buildnum = '%d'"  % (int(id), int(buildnum)))
        result = cursor.fetchall()
        if result:
            return False
        else:
            return True
    except:
        pass
    db.close()


#通过id获取jobname
def get_jobname(id):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT jobname FROM jenkc_jobsnamedes WHERE id = '%d' " % int(id))
        result = cursor.fetchall()
        jobname = result[0][0]
        return jobname
    except:
        pass
    db.close()


#给buildhistory表插入数据
def insert_build_history(jobname, buildtime, buildnum, status):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    id = select_jobname(jobname)
    if id and select_num(id, buildnum):
        print(id,jobname, buildtime, buildnum, status)
        cursor.execute("INSERT INTO jenkc_buildhistory(buildtime, buildnum, status, jobname_id)  \
        VALUES  ('%s', '%d', '%s', '%d')" % (buildtime, int(buildnum), status, int(id)))
        db.commit()
    else:
        print("%s 不存在或者 %d 历史记录已经存在" % (jobname, int(buildnum)))
    db.close()


#获取JOBASEINFO的所有信息
def get_all_data():
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM JOBASEINFO")
        results = cursor.fetchall()
    except:
        pass
    db.close()
    return results


def get_data_fromhistory(begintime, endtime):
    db = pymysql.connect(config.HOST, config.USER, config.PASSWD, config.DB)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM jenkc_buildhistory")
        results = cursor.fetchall()
    except:
        pass
    db.close()
    jobbuildhistory = []
    jobidlist = []
    for i in results:
        bt = datetime.datetime.strptime(begintime, "%Y-%m-%d %H:%M:%S")
        et = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")
        dt = i[1]
        if dt >= bt and dt <= et:
            if i[3] == 'SUCCESS':
                jobidlist.append(i[4])
        else:
            pass
    jobidset = set(jobidlist)
    for item in jobidset:
        jobuildcount = {}
        jobname = get_jobname(item)
        jobuildcount[jobname] = jobidlist.count(item)
        jobbuildhistory.append(jobuildcount)
    return jobbuildhistory


if __name__ == '__main__':
#    get_jobname(12)
    get_data_fromhistory("2018-10-22 14:44:22", "2018-11-01 14:44:22")