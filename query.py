#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import requests
from threading import Timer
import datetime

"""
自行登录 https://bm.ruankao.org.cn/index.php/query/score 获取Cookie

Cookie 必填项目为PHPSESSID、SERVERID、acw_tc
"""
headers = {
    'Cookie': ''
}
# 登录 http://www.pushplus.plus/ 将token填入
PUSH_TOKEN = ''
# 循环间隔秒数
SLEEP_SECOND = 600


def push(r, title=None):
    data = {'token': PUSH_TOKEN,
            'template': 'json',
            'title': title,
            'content': json.dumps(r)
            }
    r = requests.post("http://www.pushplus.plus/send", data=data)
    print(r.text)
    return


def get_info(taskID=100002230302151239194259):
    r = requests.post("https://bm.ruankao.org.cn/my/myscore/getinfo",
                      data={'ExamTaskID': taskID}, headers=headers)

    rk = {}
    if r.text.startswith("<!DOCTYPE html>"):
        rk.update({"Cookie": "已失效，请重新获取!"})
        print(rk)
        if len(PUSH_TOKEN) == 32:
            push(rk, 'Cookie失效啦')
        return
    rs = json.loads(r.text)
    print("查询时间：%s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if rs['flag'] == '1':
        rs = rs['data'][0]
        rk.update({'考试时间': rs['TaskName']})
        rk.update({'资格名称': rs['ProfessionName']})
        rs = rs['Score']
        for r in rs:
            if r['Score'] != "-" and float(r['Score']) >= 45:
                r['Score'] += " -> pass"
            rk.update({r['SubjectName']: r['Score']})
        print(rk)
        if len(PUSH_TOKEN) == 32:
            push(rk, '成绩出来啦')
    else:
        print(rs)
        if rs['msg'] == '暂无成绩':
            loop_get_info(SLEEP_SECOND)


def loop_get_info(s=600):
    t = Timer(s, get_info)
    t.start()


if __name__ == '__main__':
    get_info()
