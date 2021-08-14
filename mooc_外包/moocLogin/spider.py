import json
import os
import random

from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from moocphonelogin import Login
import pathlib
import requests
import time


class Spier():

    def __init__(self):
        self.session = Login().login()

    def timestamp(self):
        timestamp = int(time.time() * 1000)
        return str(timestamp)

    def get_csrfKey(self):
        self.csrfKey = dict_from_cookiejar(self.session.cookies)["NTESSTUDYSI"]
        self.session.headers.update({"edu-script-token": self.csrfKey})

    def filejudge(self, path):
        dirpath = pathlib.Path(path)
        if dirpath.exists() == False:
            dirpath.mkdir()

    def courejudge(self, course_id):
        data = {
            'callCount': 1,
            'scriptSessionId': '${scriptSessionId}190',
            'httpSessionId': self.csrfKey,
            'c0-scriptName': 'CourseBean',
            'c0-methodName': 'startTermLearn',
            'c0-id': '0',
            'c0-param0': f'string:{course_id}',
            'c0-param1': 'null:null',
            'batchId': self.timestamp(),
        }
        url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.startTermLearn.dwr'
        r = self.session.post(url=url, data=data)
        print(r.text)

    def get_Paperid(self, course_id):
        url = f"https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc?csrfKey={self.csrfKey}"
        data = {
            "termId": course_id
        }
        response = self.session.post(url=url, data=data)
        # print(response.text)
        mocTermDto = response.json()["result"]["mocTermDto"]
        Paperdict = {}
        chapters = mocTermDto["chapters"]
        courseName = mocTermDto['courseName']
        for chapter in chapters:
            contentType = chapter["contentType"]
            if contentType == 2:
                name = chapter["name"]
                id = chapter["id"]
                Paperdict[name] = {'id': id, 'isExercise': False}

            else:
                lessons = chapter["lessons"]
                quizs = chapter["quizs"]
                if lessons != None or lessons != []:
                    for lesson in lessons:
                        units = lesson["units"]
                        for unit in units:
                            unitname = unit["name"]
                            contentType = unit["contentType"]
                            contentId = unit["contentId"]
                            if contentType == 5:
                                Paperdict[unitname] = {
                                    'id': contentId,
                                    'isExercise': True
                                }
                if quizs == None or quizs == []:
                    pass
                else:
                    quizs = quizs[0]
                    quizname = quizs["name"]
                    contentId = quizs["contentId"]
                    Paperdict[quizname] = {
                        'id': contentId,
                        'isExercise': False
                    }
        exams = mocTermDto['exams']
        for exam in exams:
            name = exam['name']
            objectTestId = exam['objectTestId']
            Paperdict[name] = {
                'id':objectTestId,
                'isExercise':False
            }

        return courseName, Paperdict

    def get_answer(self, id):
        data = {
            "mob-token": "5c9fe57cd949cd5085238071d68045f7f0ebd1f67c14f38088ac00221794ff1ea42ecaa6ad9f5532ad621e93428ba04c8f2e3c413ba433abc14d0a5ef079d7edfd34c8b679acad342910d87ab08756803fe82d8881bd18d30e2ebd9980e23f4b0d7ef1ee30366d043e17db84286433cef47cc69a37661c387840ae5ab48fff24dcedc03c81e4504e3ce344d990d018b3e175e687fbea8a7f450b2b4c2eb2b4c28676b27e0d374f2f0db184284eeb568ef068144cfcbaf5b449620a83b20dcbf5",
            "testId": id,
            "isExercise": "true",
            "withStdAnswerAndAnalyse": "true"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'user-agent': "Dalvik/2.1.txt.0 (Linux; U; Android 8.1.txt.0; Pixel Build/OPM4.171019.021.P1)",
        }
        url = "https://www.icourse163.org/mob/course/paperDetail/v1"
        response = requests.post(url, data=data, headers=headers)
        answer = response.json()
        return answer

    def download(self, Paperdict, path):
        for name, dic in Paperdict.items():
            filepath = f'{path}/{name}.txt'
            pathjudge = pathlib.Path(filepath)
            if pathjudge.exists() == False:
                id = dic['id']
                answer = self.get_answer(id)
                try:
                    if answer != None:
                        with open(filepath, 'w') as f:
                            f.write(json.dumps(answer, indent=4))
                        print(f' {filepath} ----->保存成功！')
                    else:
                        print(f' {name} 无答案！')
                except:
                    print(f' {name} 无答案！')
                time.sleep(random.random())
            else:
                print(f' {filepath} 已经保存')

    def spider(self, course_id):
        self.get_csrfKey()
        self.courejudge(course_id)
        try:
            courseName, Paperdict = self.get_Paperid(course_id)
            # print(Paperdict)
            if Paperdict == {}:
                print(f' {courseName} 暂时还没有测验！')
            else:
                path = f'download/{courseName}'
                self.filejudge('download')
                self.filejudge(path)
                self.download(Paperdict,path)
            print(f' {courseName} 处理完毕！')
        except:
            print('该课程无法获取，已经关闭或者要认证为该校学生等情况')

d = Spier()
# 电磁场
# tid = '1463181451'
# c语言
# tid = '1463264446'
# 概率论
# tid = '1450241479'
# 柯南
# tid = '1465188448'



# tid = '1458392442'
# tid = '1464329463'
# tid = '1462208453'
# d.spider(tid)
tid = '1464329463'
d.get_csrfKey()
d.courejudge(tid)



# https://www.icourse163.org/spoc/course/SCXD-1457870167?tid=1458392442
# https://www.icourse163.org/course/CHD-1461568163?tid=1464329463