# -*- encoding: utf-8 -*-

import requests
import pathlib
import json
import random
from time import sleep
import re

class Mooc():

    def __init__(self):
        self.mob_token = "5c9fe57cd949cd5085238071d68045f7f0ebd1f67c14f38088ac00221794ff1ea42ecaa6ad9f5532ad621e93428ba04c8f2e3c413ba433abc14d0a5ef079d7edfd34c8b679acad342910d87ab08756803fe82d8881bd18d30e2ebd9980e23f4b0d7ef1ee30366d043e17db84286433cef47cc69a37661c387840ae5ab48fff24dcedc03c81e4504e3ce344d990d018b3e175e687fbea8a7f450b2b4c2eb2b4c28676b27e0d374f2f0db184284eeb568ef068144cfcbaf5b449620a83b20dcbf5"

    def filejudge(self, path):
        dirpath = pathlib.Path(path)
        if dirpath.exists() == False:
            dirpath.mkdir()

    def get_courseId(self, cid, tid):
        Paperdict = {}
        data = {
            "mob-token": self.mob_token,
            "tid": tid,
            "cid": cid,
        }
        url = "https://www.icourse163.org/mob/course/courseLearn/v1"
        response = requests.post(url=url, data=data)
        results = response.json()['results']
        print(results)
        termDto = results['termDto']
        chapters = termDto['chapters']
        for chapter in chapters:
            contentType = chapter["contentType"]
            if contentType == 2:
                chaptername = chapter["name"]
                id = chapter["id"]
                Paperdict[chaptername] = {'id': id, 'isExercise': False}

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
        exams = termDto['exams']
        try:
            for exam in exams:
                name = exam['name']
                objectTestId = exam['objectTestId']

                if objectTestId != None:
                    Paperdict[name] = {
                        'id': objectTestId,
                        'isExercise': False
                    }
                else:
                    subjectTestId = exam['subjectTestId']
                    Paperdict[name] = {
                        'id': subjectTestId,
                        'isExercise': False
                    }
        except:
            pass
        courseDto = results['courseDto']
        courseName = courseDto['name']
        schoolName = courseDto['schoolName']
        return schoolName, courseName, Paperdict

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
                sleep(random.random())
            else:
                print(f' {filepath} 已经保存')

    def runId(self, cid, tid):
        schoolName, courseName, Paperdict = self.get_courseId(cid=cid, tid=tid)
        if Paperdict != {}:
            print(f' {courseName} {schoolName} 开始处理！\n')
            path = f"download\{courseName}_{schoolName}"
            self.filejudge('../download')
            self.filejudge(path)
            self.download(Paperdict, path)
            print(f'\n {courseName} {schoolName} 处理完毕！')
        else:
            print(f' {courseName} {schoolName} 暂时还没有测验！')

    def runLink(self, link):
        cid, tid = re.findall('.*?/\w+-(\d+)\?tid=(\d+)', link)[0]
        schoolName, courseName, Paperdict = self.get_courseId(cid=cid, tid=tid)
        print(Paperdict)
        if Paperdict != {}:
            print(f' {courseName} {schoolName} 开始处理！\n')
            path = f"download/{courseName}_{schoolName}"
            self.filejudge('download')
            self.filejudge(path)
            self.download(Paperdict, path)
            print(f'\n {courseName} {schoolName} 处理完毕！')
        else:
            print(f' {courseName} {schoolName} 暂时还没有测验！')

d = Mooc()
# # link = 'https://www.icourse163.org/spoc/course/SYXX13-1451859164?tid=1452277444'
link = 'https://www.icourse163.org/learn/HIT-1002533005?tid=1463181451#/learn/examlist'
d.runLink(link)