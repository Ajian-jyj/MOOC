# -*- encoding: utf-8 -*-
# @Time    : 2021/8/12 17:51
# @Author  : Esword
# @Email   : jyj349559953@qq.com
# @File    : id.py
# @Software: PyCharm
# @公众号   :  spider
import json
import os
import pathlib
import re

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


def get_courseUrl_list():
    url = 'https://www.icourse163.org/university/view/all.htm'
    response = requests.get(url=url, headers=headers)
    text = response.text
    url_list = re.findall('<a class="u-usity f-fl" href="(.*?)" target="_blank"', text)
    courseUrl_list = ['https://www.icourse163.org' + i for i in url_list]
    return courseUrl_list


def get_scoolId_list(courseUrl_list):
    scoolId_list = []
    for courseUrl in courseUrl_list:
        response = requests.get(url=courseUrl, headers=headers)
        text = response.text
        schoolId = re.findall('window.schoolId = "(\d+)";', text)[0]
        print(schoolId)
        scoolId_list.append(schoolId)
    return scoolId_list


def get_pages(url, data):
    headers = {
        'authority': 'www.icourse163.org',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'edu-script-token': '8ee6e04791fc4320b155c3614b34e182',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://www.icourse163.org',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        # 'referer': 'https://www.icourse163.org/university/PKU',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'EDUWEBDEVICE=f2c5a63bcdea4834bb3b33955ab50e7e; WM_TID=SXsSiknPTKdEUVERUEcvywtgcKhfUfB2; __yadk_uid=l95WdrPGC2zPM6KkNEvs7y1nPfJFyi7d; MOOC_PRIVACY_INFO_APPROVED=true; WM_NI=Blyo%2FNAE%2B7gBZO3sdibFlb3En%2BdueZVwVgQdOmhL3TD1r31L5%2FJOlt2JNuWVQFP6u2i3ZrY1Gs0QuEfifxNlSahcFkwXIksZyTctmPhBjC%2BuK%2FSTC6nnUjm%2Bs%2BQrV%2B2xUWY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7f9729788fda8b24ebb9a8ab2c15f969b9babf539f4aaa2b0b84e96e7fb8ff52af0fea7c3b92a82b4b790ae46839be5d8e64a9a91fd94e763a29aa483b24faef5ac96e85296a99a88d4708db3a8adb26088efbed4b448f7f186b0ef80f2968296d65e939aa0d7f83aabed9693dc3b85ad00b2f84fa6b7aa99cd6891bfa884c561b588878cf252bb8cad95f05cac9ea6a4aa7f89f19db5c23eaeb29b8bf021b1f59f93d521f2a89bb8dc37e2a3; NTESSTUDYSI=8ee6e04791fc4320b155c3614b34e182; STUDY_INFO="yd.369ee6a5f4bd4d558@163.com|8|1398840432|1628836059228"; STUDY_SESS="dGJE5pTBzoHZKE+DPQ7xxxcz6S1MRmzLpp0Z6Uh4R/ZiKcORdk3z2FLq0wiAJMM53LbTBLxrwM6CwXr6oCpdDWn84PVXNkV5evcNWMIaGVDvvK6t9aRohLJ9yFxPhG9UVAw0IdEKiSlyiF6d0SGDFemojXDKf5U9uX9ZqhRWaUMLhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; STUDY_PERSIST="TpEEWcP4xy6Grjh8P7LjfgcR2l4nhjYyshNcxN/DOdReZwtot79i+jBh75XAu3M9xHI/crmgHisYa5GFjmP7IOY8LemKSpptEsJGtj+7R5GyOZusGr8ajoapM/EH4zDZO3g8ko6OcwrZre3FDMv1xjbKkmQuZOcGLKy1wiS+QiJTlrcW7yyKqyQmEeMq39Oy90js7QKFnlVTdnL7MZ3/0gmrYdrltkmU3bnLAdUPz73ZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8+tZRDonbf7gEH7JU="; NETEASE_WDA_UID=1398840432#|#1568004200078; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1628777669,1628778663,1628823884,1628836062; CLIENT_IP=61.130.109.201; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1628848842',
    }
    response = requests.post(url, headers=headers, data=data)
    pages = response.json()['result']['query']['totlePageCount']
    return pages


def get_tid(schoolId):
    headers = {
        'authority': 'www.icourse163.org',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'edu-script-token': '8ee6e04791fc4320b155c3614b34e182',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://www.icourse163.org',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        # 'referer': 'https://www.icourse163.org/university/PKU',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'EDUWEBDEVICE=f2c5a63bcdea4834bb3b33955ab50e7e; WM_TID=SXsSiknPTKdEUVERUEcvywtgcKhfUfB2; __yadk_uid=l95WdrPGC2zPM6KkNEvs7y1nPfJFyi7d; MOOC_PRIVACY_INFO_APPROVED=true; WM_NI=Blyo%2FNAE%2B7gBZO3sdibFlb3En%2BdueZVwVgQdOmhL3TD1r31L5%2FJOlt2JNuWVQFP6u2i3ZrY1Gs0QuEfifxNlSahcFkwXIksZyTctmPhBjC%2BuK%2FSTC6nnUjm%2Bs%2BQrV%2B2xUWY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7f9729788fda8b24ebb9a8ab2c15f969b9babf539f4aaa2b0b84e96e7fb8ff52af0fea7c3b92a82b4b790ae46839be5d8e64a9a91fd94e763a29aa483b24faef5ac96e85296a99a88d4708db3a8adb26088efbed4b448f7f186b0ef80f2968296d65e939aa0d7f83aabed9693dc3b85ad00b2f84fa6b7aa99cd6891bfa884c561b588878cf252bb8cad95f05cac9ea6a4aa7f89f19db5c23eaeb29b8bf021b1f59f93d521f2a89bb8dc37e2a3; NTESSTUDYSI=8ee6e04791fc4320b155c3614b34e182; STUDY_INFO="yd.369ee6a5f4bd4d558@163.com|8|1398840432|1628836059228"; STUDY_SESS="dGJE5pTBzoHZKE+DPQ7xxxcz6S1MRmzLpp0Z6Uh4R/ZiKcORdk3z2FLq0wiAJMM53LbTBLxrwM6CwXr6oCpdDWn84PVXNkV5evcNWMIaGVDvvK6t9aRohLJ9yFxPhG9UVAw0IdEKiSlyiF6d0SGDFemojXDKf5U9uX9ZqhRWaUMLhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; STUDY_PERSIST="TpEEWcP4xy6Grjh8P7LjfgcR2l4nhjYyshNcxN/DOdReZwtot79i+jBh75XAu3M9xHI/crmgHisYa5GFjmP7IOY8LemKSpptEsJGtj+7R5GyOZusGr8ajoapM/EH4zDZO3g8ko6OcwrZre3FDMv1xjbKkmQuZOcGLKy1wiS+QiJTlrcW7yyKqyQmEeMq39Oy90js7QKFnlVTdnL7MZ3/0gmrYdrltkmU3bnLAdUPz73ZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8+tZRDonbf7gEH7JU="; NETEASE_WDA_UID=1398840432#|#1568004200078; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1628777669,1628778663,1628823884,1628836062; CLIENT_IP=61.130.109.201; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1628848842',
    }
    cid_tid_dic = {}
    schoolName = ''
    # 学校云
    url = 'https://www.icourse163.org/web/j/courseBean.searchSchoolCloudCourseList.rpc?csrfKey=8ee6e04791fc4320b155c3614b34e182'
    data = {
        'schoolId': schoolId,
        'p': '1',
        'psize': '20',
        'courseStatus': '30',
        'categoryId': '-1',
        'resourceId': '-1'
    }
    pages = get_pages(url, data)
    for p in range(1, pages + 1):
        data['p'] = p
        response = requests.post(url, headers=headers, data=data)
        list = response.json()['result']['list']
        if list != None:
            for i in list:
                cid = i['id']
                tid = i['currentTermId']
                cid_tid_dic.update({cid: tid})
                schoolName = i['schoolName']

    # 学校
    url = 'https://www.icourse163.org/web/j/courseBean.getCourseListBySchoolId.rpc?csrfKey=8ee6e04791fc4320b155c3614b34e182'
    data = {
        'schoolId': schoolId,
        'p': '1',
        'psize': '20',
        'type': '1',
        'courseStatus': '30'
    }
    pages = get_pages(url, data)
    for p in range(1, pages + 1):
        data['p'] = p
        response = requests.post(url, headers=headers, data=data)
        list = response.json()['result']['list']
        if list != None:
            for i in list:
                cid = i['id']
                tid = i['currentTermId']
                cid_tid_dic.update({cid: tid})
                schoolName = i['schoolName']

    path = f'id/{schoolName}.txt'
    with open(path, 'w') as f:
        f.write(json.dumps(cid_tid_dic, indent=4))
    print(f'{path} 完成！')

    return cid_tid_dic, schoolName


if __name__ == '__main__':
    path = pathlib.Path('id')
    if path.exists() == False:
        path.mkdir()
    # courseUrl_list = get_courseUrl_list()
    # scoolId_list = get_scoolId_list(courseUrl_list)
    scoolId_list = ['13001', '9002', '6001', '9003', '8011', '9010', '8007', '9020', '9018', '9022', '9006', '9004',
                    '8009', '8008', '9005', '8012', '8013', '8003', '8015', '9011', '9009', '9001', '8002', '8005',
                    '8004', '9008', '8006', '9019', '8014', '8010', '9015', '9014', '9012', '9013', '9007', '9017',
                    '9021', '9016', '1001176003', '20002', '1001171002', '57001', '74001', '75001', '101001', '110001',
                    '113001', '1001175001', '1001298001', '1001353001', '1001439001', '1001568001', '1001569001',
                    '1001617001', '1001621001', '1203066801', '63001', '1001396001', '1001437002', '1001171001',
                    '1001212001', '1001220001', '1001316001', '98001', '112001', '59001', '1001214001', '90002',
                    '1203062801', '1001167002', '38001', '46001', '1203010801', '1001237008', '28001', '67002', '88002',
                    '47001', '53001', '1001188001', '1001238001', '1001239001', '36001', '116001', '52002', '68001',
                    '1001239004', '49001', '103001', '104001', '105001', '106001', '39001', '1001177001', '1001195001',
                    '108002', '35001', '122001', '1001449002', '108003', '1001268003', '109001', '140001', '1001170001',
                    '94001', '132001', '150001', '1001391001', '1444116161', '1444135164', '1444146162', '1444501161',
                    '1203198801', '20001', '1001330001', '1203077802', '125001', '1001460001', '1001289001',
                    '1203033801', '131003', '1001222001', '1001440001', '1203099801', '1444547162', '1202994801',
                    '1001397001', '1001399001', '1001309001', '52001', '1001196001', '1202954801', '1001495003',
                    '1202998802', '1203127801', '1001609001', '1001502001', '1001518001', '1202984801', '1001319001',
                    '1203098801', '1001224001', '1001426001', '108001', '1001501001', '1001591003', '1203207801',
                    '1001200001', '1202976801', '50001', '54001', '1001577001', '1203051801', '1202995801',
                    '1001532001', '1001477001', '1001179001', '107001', '146001', '1001237004', '117001', '1001238004',
                    '1001237005', '30001', '13002', '55001', '1202958801', '1001208001', '121001', '1001338001',
                    '1001224002', '1444525161', '1202970801', '1444070165', '1001254002', '1001251001', '1001328001',
                    '1202999802', '1001255001', '1001250001', '1203055801', '64001', '1001572001', '1001478001',
                    '86002', '1001183001', '1001612001', '1001194001', '1001264004', '114001', '1001293001',
                    '1001531001', '1001303001', '1001524001', '1001580001', '119002', '1202960801', '44001',
                    '1001248001', '1202993802', '1001325001', '1001245001', '125002', '1001229003', '1001216002',
                    '1001215001', '1001176002', '48002', '141001', '1001425001', '87002', '1001442001', '1001349001',
                    '1202966801', '1001342001', '1203070801', '1001392001', '1001380001', '1001441001', '1001305001',
                    '1203020801', '1001379001', '119001', '1001410001', '1001463002', '1001173001', '1001265005',
                    '1001462001', '161001', '115001', '1202962801', '1001489004', '1001204001', '1001168001',
                    '1001172001', '1202967801', '165001', '1202987802', '102001', '1202996801', '1001346001',
                    '1001169001', '97001', '1001497002', '66001', '1001177002', '1001423001', '1202977801',
                    '1203069802', '153001', '1444051161', '1444050161', '1203083801', '1203084801', '1203067802',
                    '1203079801', '1203097801', '1444131165', '1444164161', '1444290161', '1444129162', '1444247161',
                    '1444338161', '1444353161', '1203081801', '1203106801', '1001571002', '1203090801', '131002',
                    '77001', '90001', '99001', '1001484002', '1001234001', '1001395001', '1001481001', '1203032801',
                    '1203060801', '1203134803', '1444153163', '129001', '1203140802', '1203189802', '1001308001',
                    '1001516001', '1203031801', '1203042801', '1203193801', '1203213801', '1444126161', '1444127161',
                    '1202959801', '1203102801', '1203138801', '1203049802', '1203126802', '1203022801', '1203028801',
                    '1203029801', '1203041801', '1203050801', '1203052801', '1203054801', '1203100801', '1203109801',
                    '1203116801', '1203118801', '1203120801', '1203139801', '1203149801', '1443972161', '1444124161',
                    '1444506161', '1444545161', '1001397007', '1001396002', '1001398002', '1203223802', '1203173801',
                    '128001', '1001508001', '1001586004', '1001463001', '1001570001', '1001585001', '1444153162',
                    '1202993801', '1203013801', '1001237003', '1001237007', '1001237011', '1001240004', '1001238003',
                    '1001238007', '40001', '1001238011', '1001239003', '1001240003', '1001243016', '1001233002',
                    '1001237002', '1001237006', '1001237010', '1001238002', '1001238006', '1001238010', '78001',
                    '1001239002', '87001', '1001239006', '89001', '1001240002', '1001590003', '93001', '96001',
                    '123001', '133001', '1001586002', '1001587002', '1001588002', '1001590002', '1001591002',
                    '1001167001', '1001209001', '1001235001', '1001237009', '1001238005', '1001238009', '1001240001',
                    '1001465001', '1001586001', '1001587001', '1001589001', '1001590001', '1001591001', '1001592001',
                    '1203155801', '1001261004', '1001262004', '1001261011', '1001261014', '1001359002', '1001361006',
                    '142001', '1001259001', '1001261009', '1001262005', '1001263001', '1001264005', '1001291001',
                    '1001337001', '1001350001', '1001365001', '1001372001', '41001', '43001', '48001', '1001215002',
                    '65001', '71001', '1001449003', '1444547760', '1001335002', '130001', '1001499002', '1001622002',
                    '1202984802', '1203008802', '1203009802', '1001187001', '1443974162', '1443993162', '1444547170',
                    '1001286001', '1001312001', '1001341001', '1001355001', '1001456001', '1001467001', '1001482001',
                    '1001557001', '1001564001', '1001584001', '1202971801', '1202972801', '1202988801', '1203038801',
                    '1203044801', '1203087801', '1203133801', '1203175801', '1203202801', '1203212801', '1444086161',
                    '1444462161', '1444535161', '1444547221', '91001', '118001', '1001176001', '1001213001',
                    '1001217001', '1001221001', '1001381001', '1001435001', '1001438001', '1001521001', '1203091801',
                    '1202983801', '1203211801']
    for schoolId in scoolId_list:
        get_tid(schoolId)

    try:
        os.remove('id/.txt')
    except:
        pass
    print(len(scoolId_list))
