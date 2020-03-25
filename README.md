# 今日校园 辅导猫 自动签到

**仅适用NEUQ**

## 使用
### 安装依赖
```
$ pip install requests
```
### 修改配置
```
$ cp config.py.example config.py 
填写账号密码 及 位置信息
```
### 运行
```
$ python3 main.py
```
### 定时任务
```
$ crontab -e    
1 8 * * * /usr/bin/python3.6 /var/www/cpdaily-auto/main.py >> /var/www/cpdaily-auto/main.log 2>&1
```

## 参考
[cpdaily_auto_signin](https://github.com/OrionAAAA/cpdaily_auto_signin)
[cpdaily-api](https://github.com/jerryshell/cpdaily-api)