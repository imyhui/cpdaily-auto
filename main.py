import config
import requests
import re

# 从文件导入账号配置
username = config.username
password = config.password
longitude = config.longitude
latitude = config.latitude
position = config.position


def get_cookies():
    session = requests.session()
    url = "http://ids.neuq.edu.cn/authserver/login?service=https%3A%2F%2Fneuq.cpdaily.com%2Fportal%2Flogin"
    headers = {
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; V9 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'zh-CN,en-US;q=0.8'
    }

    # 获取登录所需参数
    response = session.get(url=url)

    addon = re.findall(
        '<input type="hidden" name="(.*?)" value="(.*?)"/?>', response.text)
    form = [
        f"username={username}",
        f"password={password}"
    ]
    for k, v in addon:
        form.append(f"{k}={v}")
    data = '&'.join(form)

    # 登录 获取cookie
    response = session.post(
        url=url,
        headers=headers,
        data=data,
    )

    try:
        cookies = requests.utils.dict_from_cookiejar(session.cookies)
        global_cookie = f"acw_tc={cookies['acw_tc']}; MOD_AUTH_CAS={cookies['MOD_AUTH_CAS']}"
    except:
        print("账号或密码错误")
        exit()
    return global_cookie


def get_signInstanceWid(global_cookie):
    url = 'https://neuq.cpdaily.com/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay'

    headers = {
        'Host': 'neuq.cpdaily.com',
        'Connection': 'keep-alive',
        'Content-Length': '2',
        'accept': 'application/json, text/plain, */*',
        'Origin': 'https://neuq.cpdaily.com',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; vivo xplay6 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 yiban/8.1.11 cpdaily/8.1.11 wisedu/8.1.11',
        'content-type': 'application/json',
        'Referer': 'https://neuq.cpdaily.com/wec-counselor-sign-apps/stu/mobile/index.html?timestamp=1584597152126',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': global_cookie
    }
    
    # 获取待签到任务ID
    body = {}
    r = requests.post(url, headers=headers, json=body)
    print(r.json())

    if r.json()['datas']['unSignedTasks'] == []:
        print("今天已签到")
        exit()
    else:
        signinstanceWid = r.json(
        )['datas']['unSignedTasks'][0]['signInstanceWid']

    return signinstanceWid


def sign_in(global_cookie):
    url = 'https://neuq.cpdaily.com/wec-counselor-sign-apps/stu/sign/submitSign'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; vivo xplay6 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 yiban/8.1.11 cpdaily/8.1.11 wisedu/8.1.11',
        'CpdailyStandAlone': '0',
        'extension': '1',
        'Cpdaily-Extension': 'CEzs4zRiNZDRs6kUbgbXcfy038GONsXOnuU5brmSNbrq779Z06Ld4aaOhJXP knEjShqKP3hIxaT3NvYekc++1so/qobhD6N9JhpdcWeQHO9SdRZiJMoY2oqs nwB2lGKX+1GAiAcR8ddEyagdfOOXKSpmQUzIUDM/+hKlEbZsm/eZUfgrJpjX ZUXdvT9WEFRT5y5GACLegKRGhs0rhdNH4iSzh2+46hyZLUiz+ep84SzD5m/q FP71ssX+ZooufKeeJ8uYpjVMZIw=',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '188',
        'Host': 'neuq.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': global_cookie
    }

    signInstanceWid = get_signInstanceWid(global_cookie)
    # print(signInstanceWid)

    body = {"signInstanceWid": signInstanceWid, "longitude": longitude, "latitude": latitude,
            "isMalposition": 1, "abnormalReason": " ", "signPhotoUrl": "", "position": position}

    # 提交签到任务
    r = requests.post(url, headers=headers, json=body)
    if r.json()['message'] == 'SUCCESS':
        print("签到成功")
        return True
    else:
        print("签到失败，有可能不在签到时间内或出现未知错误。请自行调试")
        return False


global_cookie = get_cookies()
# print(global_cookie)
sign_in(global_cookie)
