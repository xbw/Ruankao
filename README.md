# Ruankao
2023年最新软考查分，内置循环无须配置crontab，支持循环间隔时间配置

支持微信公众号、企微机器人、钉钉机器人提醒，可自由搭配提醒方式


## 安装
- 运行环境：Python3+，以上代码在 3.8.10 版本测试成功
- 安装第三方库：pip install -r requirements.txt


## 运行
- 必须：
    - 自行登录 [成绩查询](https://bm.ruankao.org.cn/index.php/query/score) 获取Cookie，填入 Cookie
- 可选
    - 支持微信公众号推送，注册 [pushplus(推送加)](http://www.pushplus.plus/) ，填入PUSHPLUS_TOKEN
    - 支持钉钉机器人推送，设置如下 [自定义机器人接入](https://open.dingtalk.com/document/isvapp/custom-bot-access-send-message)，填入DINGTALK_ACCESS_TOKEN和DINGTALK_SECRET
    - 支持企微机器人推送，设置如下 [如何设置群机器人 ](https://open.work.weixin.qq.com/help2/pc/14931)，填入WECHAT_KEY
    - 
    - 循环间隔时间默认为600秒(10分钟)，如需修改直接修改 [SLEEP_SECOND] 值

## Contributing

Pull requests for new features, bug fixes, and suggestions are welcome!


## License

[MIT](https://github.com/xbw/Ruankao/blob/master/LICENSE)

Copyright (c) 2017-present xbw