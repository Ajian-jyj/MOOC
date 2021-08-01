# -*- encoding: utf-8 -*-
"""
@File    :   show.py    
@Contact :   jyj345559953@qq.com
@Author  :   Esword
"""

from requests.utils import dict_from_cookiejar
from rich.console import Console
console = Console()

class courseShow():

    def __init__(self,session):
        self.session = session

    def get_csrfKey_userId(self):
        self.userId = dict_from_cookiejar(self.session.cookies)["NETEASE_WDA_UID"].split('#')[0]
        params = {
            "userId": self.userId
        }
        self.session.get('https://www.icourse163.org/home.htm', params=params)
        self.csrfKey = dict_from_cookiejar(self.session.cookies)["NTESSTUDYSI"]
        self.session.headers.update({"edu-script-token": self.csrfKey})
        return

    def get_pagesize(self):
        url = "https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc"
        params = {
            "csrfKey": self.csrfKey
        }
        data = {
            'type': '30',
            'p': '1',
            'psize': '8',
            'courseType': '1',
        }
        response = self.session.post(url=url, params=params, data=data)
        pagesize = response.json()["result"]["pagination"]["totlePageCount"]
        return int(pagesize)

    def get_courses(self, pagesize):
        courses_dic = {}
        url = "https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc"
        params = {
            "csrfKey": self.csrfKey
        }
        for p in range(1, pagesize):
            data = {
                "type": "30",
                "p": p,
                "psize": '8',
                "courseType": "1",
            }
            response = self.session.post(url, data=data, params=params)
            result = response.json()["result"]["result"]
            courses_dic[str(p)] = {}
            n_key = 1
            try:
                for i in result:
                    course_name = i["name"]
                    courses_id = i["termPanel"]["id"]
                    school_name = i["schoolPanel"]["name"]
                    list = [courses_id,course_name, school_name]
                    courses_dic[str(p)][str(n_key)] = list
                    n_key += 1
            except:
                pass
        return courses_dic

    def show(self):
        self.get_csrfKey_userId()
        pagessize = self.get_pagesize()
        courses_dic = self.get_courses(pagessize)

        for Key, Value in courses_dic.items():
            console.print(f":smiley: 第{Key}页 :smiley:\n")
            console.print(Value)
            print("\n按enter键即可实现翻页\n")
            num = input("请输入课程序号:")
            try:
                if num in Value.keys():
                    courses_id = courses_dic[Key][num][0]
                    courses_name = courses_dic[Key][num][1]
                    courses_school = courses_dic[Key][num][2]
                    return courses_id,courses_name,courses_school
            except:
                pass

# c = courseShow()
# c.show()