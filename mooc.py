# -*- encoding: utf-8 -*-
"""
@File    :   main.py    
@Contact :   jyj345559953@qq.com
@Author  :   Esword
"""
import os
from download import Download
from login import Applogin
from show import courseShow
from rich.console import Console
from rich.table import Table


def main():
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.title_style = "red"
    table.title = "慕课下载器"
    table.add_column("Author", style="cyan", no_wrap=True)
    table.add_column("Mail", style="green")
    table.add_row(
        "                      ", "                                 "
    )
    table.add_row(
        "[bold]Esword[/bold]   ", "[bold]jyj349559953@qq.com[/bold] "
    )
    table.add_row(
    )
    console.print(table)
    console.print("喜欢可以关注我的公众号spiders(头像小蜘蛛)", style="red")
    # 公众号图片显示
    os.system("python .\core\wx.py")
    session = Applogin().login()
    moviebool = int(input("\n是否下载视频|[1/0]?->"))
    databool = int(input("是否下载pdf等资料|[1/0]?->"))
    paperbool = int(input("是否下载测验|[1/0]?->"))
    discussbool = int(input("是否下载讨论|[1/0]?->"))
    if moviebool == 1:
        moviebool = True
        print("1为标清\n"
              "2为高清\n"
              "3为超清")
        quality = int(input("请输入要下载视频的画质:->"))
    else:
        moviebool =False
        quality = 1

    if databool == 1:
        databool = True
    else:
        databool =False

    if paperbool == 1:
        paperbool = True
    else:
        paperbool = False

    if discussbool == 1:
        discussbool = True
    else:
        discussbool = False


    b = os.path.exists('data')
    if b == False:
        os.mkdir('data')
    courseshow = courseShow(session)
    donwnload = Download(session)
    courses_id,courses_name,courses_school = courseshow.show()
    basePath = f"data\{courses_name}_{courses_school}"
    b = os.path.exists(basePath)
    if b == False:
        os.mkdir(basePath)
    donwnload.download_main(basePath,courses_id,quality, moviebool,databool, paperbool,discussbool)

if __name__ == '__main__':
    main()

# pyinstaller -F -i E:\Users\jyj34\Desktop\yjtp.ico E:\PycharmProjects\dabao\mooc\mooc.py -p E:\PycharmProjects\dabao\mooc