# -*- encoding: utf-8 -*-

import random
import re
import time
import requests

def get_cid_tid(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    response = requests.get(url=url, headers=headers)
    text = response.text
    schoolShortName = re.findall('shortName:"(.*?)",',text)[-1]
    # if schoolShortName == None:
    #     schoolShortName = re.findall('learn/(.*?)-',url)[0]
    print(schoolShortName)
    # print(url)
    url = f'https://www.icourse163.org/university/{schoolShortName}'
    response = requests.get(url=url, headers=headers)
    text = response.text
    schoolId = re.findall('window.schoolId = "(\d+)";',text)[0]
    with open("schoolId.txt", "a+") as f:
        f.write(schoolId+'\n')
    return schoolId

f = open("课程链接.txt")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法
while line:
    line = f.readline()
    url = line.strip()
    schoolId = get_cid_tid(url=url)
    print(schoolId)
    print('------------------')
    time.sleep(random.random())

f.close()


