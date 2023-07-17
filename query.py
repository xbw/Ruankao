#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import requests
from threading import Timer
import datetime
import time
import hmac
import hashlib
import base64
import urllib.parse

"""
自行登录 https://bm.ruankao.org.cn/index.php/query/score 获取Cookie

Cookie 必填项目为PHPSESSID、SERVERID、acw_tc
"""
headers = {
    'Cookie': ''
}
# 微信公众号推送
# http://www.pushplus.plus/ 将token填入
PUSHPLUS_TOKEN = ''

# 钉钉机器人
# https://open.dingtalk.com/document/isvapp/custom-bot-access-send-message
DINGTALK_ACCESS_TOKEN = ''
DINGTALK_SECRET = ''

# 企微机器人
# https://open.work.weixin.qq.com/help2/pc/14931
WECHAT_KEY = ''

# 循环间隔秒数
SLEEP_SECOND = 600


def pushplus(content, title=None):
    data = {
        'token': PUSHPLUS_TOKEN,
        'template': 'json',
        'title': title,
        'content': content
    }
    r = requests.post("http://www.pushplus.plus/send", json=data, headers={"Content-Type": "application/json"})
    # print(r.text)
    return r


def dingtalk(content='ding'):
    timestamp = str(round(time.time() * 1000))
    secret_enc = DINGTALK_SECRET.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, DINGTALK_SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://api.dingtalk.com/robot/send?access_token={DINGTALK_ACCESS_TOKEN}&timestamp={timestamp}&sign={sign}'
    data = {
        'msgtype': 'text',
        'text': {'content': content},
        "at": {
            "isAtAll": True
        }
    }
    r = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return r


def wechat(content='wechat'):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WECHAT_KEY}'
    data = {
        'msgtype': 'text',
        'text': {
            'content': content,
            "mentioned_list": ["@all"],
            "mentioned_mobile_list": ["@all"]
        }
    }
    r = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return r


def push(content, title=None):
    print(content)

    if len(PUSHPLUS_TOKEN) == 32:
        pushplus(content, title)

    if len(DINGTALK_ACCESS_TOKEN) > 0 and len(DINGTALK_SECRET) > 0:
        dingtalk(content)

    if len(WECHAT_KEY) > 0:
        wechat(content)

    return


def score(taskID=100002230302151239194259):
    r = requests.post("https://bm.ruankao.org.cn/my/myscore/getinfo",
                      data={'ExamTaskID': taskID}, headers=headers)
    if r.text.startswith("<!DOCTYPE html>"):
        push("Cookie已失效，请重新获取!", 'Cookie失效啦')
    else:
        rs = json.loads(r.text)
        print("查询时间：%s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if rs['flag'] == '1':
            content = {}
            rs = rs['data'][0]
            content.update({'考试时间': rs['TaskName']})
            content.update({'资格名称': rs['ProfessionName']})
            rs = rs['Score']
            for r in rs:
                if r['Score'] != "-" and float(r['Score']) >= 45:
                    r['Score'] += " -> pass"
                content.update({r['SubjectName']: r['Score']})
            push(content, '成绩出来啦')
        else:
            print(rs)
            if rs['msg'] == '暂无成绩':
                loop_score(SLEEP_SECOND)


def loop_score(sleep=600):
    timer = Timer(sleep, score)
    timer.start()


if __name__ == '__main__':
    score()
