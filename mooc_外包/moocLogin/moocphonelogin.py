# -*- encoding: utf-8 -*-

import base64
import json
import os
import re
import time
from time import sleep
import js2py
import requests
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.PublicKey import RSA
from requests.utils import dict_from_cookiejar, cookiejar_from_dict


class Login():

    def __init__(self):
        self.username = '15099215030'
        self.password = 'txy15099215030'
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }

    def timestamp(self):
        timestamp = int(time.time() * 1000)
        return timestamp

    def reade_cookie(self):
        b = os.path.exists("core/cookies.json")
        if b == False:
            return False
        else:
            try:
                with open(r'core/cookies.json', 'r') as f:
                    cookie_dic = json.loads(f.read())
                cookie_jar = cookiejar_from_dict(cookie_dic)
                self.session.cookies = cookie_jar
                return True
            except:
                return False

    def save_cookie(self):
        cookie_jar = self.session.cookies
        cookie_dic = dict_from_cookiejar(cookie_jar)
        with open('core/cookies.json', 'w') as f:
            f.write(json.dumps(cookie_dic))

    def check_cookie(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        }
        try:
            data = {
                'loginType': '8'
            }
            url = f'https://www.icourse163.org/web/j/memberBean.getBindStatusByLoginType.rpc?csrfKey={self.get_csrfKey()}'
            response = self.session.post(url=url,data=data,headers=headers)
            if response.json()['result'] == True:
                print('cookie有效')
                return True
            else:
                print('cookie无效')
                return False
        except:
            print('无效cookie')
            return False

    def get_csrfKey(self):
        csrfKey = dict_from_cookiejar(self.session.cookies)["NTESSTUDYSI"]
        self.session.headers.update({"edu-script-token": csrfKey})
        return csrfKey

    def Rtid(self):
        context = js2py.EvalJs()
        js = '''
            function rtid() {
                var e = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                  , t = 32
                  , i = [];
                for (; t-- > 0; )
                    i[t] = e.charAt(Math.random() * e.length);
                return i.join("")
            };
        '''
        context.execute(js)
        rtid = context.rtid()
        return rtid

    def pw(self):
        message = self.password.encode('utf-8')
        publicKey = """-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB\n-----END PUBLIC KEY-----"""
        rsakey = RSA.importKey(publicKey)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        pw = base64.b64encode(cipher.encrypt(message)).decode('utf-8')
        return pw

    def front_tk(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }
        url_cookie = 'https://reg.icourse163.org/dl/yd/ini?pd=imooc&pkid=cjJVGQM&pkht=www.icourse163.org&channel=1&topURL=https%3A%2F%2Fwww.icourse163.org%2F&rtid=' + self.rtid + f'&nocache={self.timestamp()}'
        res = self.session.get(url_cookie, headers=headers)
        self.session.cookies = res.cookies

    def tk(self):
        self.front_tk()
        params = {
            'un': self.username,
            'channel': 1,
            'pd': 'imooc',
            'pkid': 'cjJVGQM',
            'topURL': 'https://www.icourse163.org/',
            'rtid': self.rtid,
            'nocache': self.timestamp(),
        }
        url = 'https://reg.icourse163.org/dl/yd/gt'
        response = self.session.get(url=url, params=params)
        tk = response.json()['tk']
        return tk

    def login_two(self):
        """
        为了获取cookies
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }

        url = 'https://www.icourse163.org/'
        response = self.session.get(url=url, headers=headers)
        html = response.content.decode()
        href_list = re.findall('href="(.*?)"',html)
        for href in href_list:
            sleep(0.75)
            self.session.get(href)

    def login_one(self):
        """
        账号密码登录
        :return:
        """
        tk = self.tk()
        # 这里 sleep 是必须的，请求过快会出错。
        sleep(2)
        pw = self.pw()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/json'
        }
        data = {
            "l": 1,
            "d": 10,
            "un": "15099215030",
            "pw": pw,
            "pd": "imooc",
            "pkid": "cjJVGQM",
            "tk": tk,
            "domains": "",
            "channel": 1,
            "topURL": "https://www.icourse163.org/",
            "rtid": self.rtid
        }
        url = 'https://reg.icourse163.org/dl/yd/lpwd'
        self.session.post(url=url, data=json.dumps(data),headers=headers)

    def login(self):
        """
        登录入口
        :return:
        """
        file_bool = os.path.exists('core')
        if file_bool == False:
            os.makedirs('core')
        reade_cookie_bool = self.reade_cookie()
        check_cookie_bool = self.check_cookie()
        if reade_cookie_bool == False or check_cookie_bool == False:
            print('正在登录...')
            self.rtid = self.Rtid()
            self.session.get('https://www.icourse163.org/')
            self.login_one()
            self.login_two()
            self.save_cookie()
            print('登录成功...')
        return self.session