# -*- encoding: utf-8 -*-

from mooc import Mooc

mooc = Mooc()

def portID(cid,tid):
    mooc.runId(cid=cid,tid=tid)

def portLink(link):
    mooc.runLink(link)

# 粉末冶金
# cid = 1461568163
# tid = 1464329463
# # 机械图样的识读与绘制(II)
# cid = 1457870167
# tid = 1458392442
# portID(cid=cid,tid=tid)

# link = 'https://www.icourse163.org/spoc/course/SCXD-1457870167?tid=1458392442'
# link = 'https://www.icourse163.org/learn/HIT-1002533005?tid=1463181451#/learn/announce'
# link = 'https://www.icourse163.org/learn/CSU-1003380004?tid=1465188448#/learn/announce'
link = 'https://www.icourse163.org/learn/ZJU-1003315004?tid=1206928208#/learn/announce'
portLink(link=link)