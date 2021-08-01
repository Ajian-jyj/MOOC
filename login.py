# -*- encoding: utf-8 -*-
"""
@File    :   login.py    
@Contact :   jyj345559953@qq.com
@Author  :   Esword
"""
import json
import os
import requests
import time
from requests.utils import dict_from_cookiejar, cookiejar_from_dict

class Applogin():

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'referer': 'https://www.icourse163.org/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',

        }

    def get_codeUrl_pollKey(self):
        self.session.get("https://www.icourse163.org/")
        url = "https://www.icourse163.org/logonByQRCode/code.do?width=182&height=182"
        response = self.session.get(url=url)
        dic = response.json()
        if dic["code"] == 0:
            print("获取codeUrl与pollKey成功")
        else:
            print("获取codeUrl与pollKey失败")
        codeUrl = dic["result"]["codeUrl"]
        pollKey = dic["result"]["pollKey"]
        return codeUrl, pollKey

    def show_QR_img(self, codeUrl):
        # os.system(f"qr {codeUrl}")
        response = self.session.get(url=codeUrl)
        content = response.content
        with open('core\QR.png', 'wb') as f:
            f.write(content)
        # os.startfile('core\QR.png')

        os.system("python .\core\QR.py")

    def get_status(self, pollKey):
        url = 'https://www.icourse163.org/logonByQRCode/poll.do?pollKey={}'.format(pollKey)
        while True:
            response = self.session.get(url=url)
            dic = response.json()
            if dic["result"]["codeStatus"] == 0:
                print("请及时扫码")
            elif dic["result"]["codeStatus"] == 1:
                print("请点击确认")
            else:
                print("登录成功")
                token = dic["result"]["token"]
                return token
            time.sleep(1)

    def save_cookie(self):
        codeUrl, pollKey = self.get_codeUrl_pollKey()
        self.show_QR_img(codeUrl)
        token = self.get_status(pollKey)
        params = {
            "token": token,
            "returnUrl": "aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcv",
        }
        url = "https://www.icourse163.org/passport/logingate/mocMobChangeCookie.htm"
        self.session.get(url=url, params=params)
        self.session.get("https://www.icourse163.org/")
        cookie_jar = self.session.cookies
        cookie_dic = dict_from_cookiejar(cookie_jar)
        with open('core/cookies.json', 'w') as f:
            f.write(json.dumps(cookie_dic))
        print("cookie已保存")

    def check_cookie(self):
        # print('正在检查cookie有效性')
        url = 'https://www.icourse163.org/'
        response = self.session.get(url=url)
        text = response.text
        if "个人中心" in text:
            # print("cookie有效")
            return True
        else:
            # print("cookie无效")
            return False

    def reade_cookie(self):
        b = os.path.exists("core/cookies.json")
        if b == False:
            print("没有cookie文件")
            return False
        else:
            with open(r'core/cookies.json', 'r') as f:
                cookie_dic = json.loads(f.read())
            cookie_jar = cookiejar_from_dict(cookie_dic)
            self.session.cookies = cookie_jar
            # print("cookie已加载")
            return True

    def login(self):
        b = os.path.exists('core')
        if b == False:
            os.mkdir('core')
        b = self.reade_cookie()
        if b == True:
            b1 = self.check_cookie()
            if b1 == False:
                # 删除存在的失效cookie
                self.session.cookies.clear()
                self.save_cookie()
                os.remove('core/QR.png')
        else:
            self.save_cookie()
            os.remove('core/QR.png')

        self.session.headers = {
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.3",
        }

        return self.session


class Wxlogin():

    def __init__(self):
        pass