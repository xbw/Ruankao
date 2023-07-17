# Ruankao
2023年最新软考查分，内置循环无须配置crontab，可配置循环间隔时间

支持微信公众号提醒，自行配置是否提醒



## 安装
- 运行环境：Python3
- 安装第三方库：pip install -r requirements.txt


## 运行
- 必须：
    - 自行登录 [成绩查询](https://bm.ruankao.org.cn/index.php/query/score) 获取Cookie，填入 Cookie
- 可选
    - 支持微信 [pushplus(推送加)](http://www.pushplus.plus/) 推送,注册后填入PUSH_TOKEN
    - 修改循环间隔时间[SLEEP_SECOND]，默认为600秒
 

## Contributing

Pull requests for new features, bug fixes, and suggestions are welcome!


## License

[MIT](https://github.com/xbw/Ruankao/blob/master/LICENSE)

Copyright (c) 2017-present xbw