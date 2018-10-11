# -*- coding:utf-8 -*-

import requests
import re
import sys
import os
from bs4 import BeautifulSoup
import Cookies

help_msg = """                                                                              
    ,@@@@@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
    ,@@@@@@@@@@@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       
    ,@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
    ,@@@@/                ,&@@@@@               ,@@@@/                     
    ,@@@@/                 ,%@@@%               ,@@@@/                     
    ,@@@@/                 ./@@@&               ,@@@@/                     
    ,@@@@/                 .(@@@&               ,@@@@/                     
    ,@@@@/                 (&@@@#               ,@@@@/                     
    ,@@@@/              ./%@@@@%,               ,@@@@/                     
    ,@@@@@@@@@@@@@@@@@@@@@@@@@&.                ,@@@@/                     
    ,@@@@@@@@@@@@@@@@@@@@@@@&*                  ,@@@@/                     
    ,@@@@@@@@@@@@@@@@@@@@@(*,                   ,@@@@/                     
    ,@@@@/                                      ,@@@@/                     
    ,@@@@/                                      ,@@@@/                     
    ,@@@@/                                      ,@@@@/                     
    ,@@@@/                                      ,@@@@/                     
    ,@@@@/                                      ,@@@@/                     
    ,@@@@/                                      .@@@@/                     
    ,@@@@/.                                     ,@@@@/                     
    ,@@@@,                                      .&@@@,
    """
print(help_msg)
f = open("1.html", "r", encoding='UTF-8')
f_content = f.read()
html_soup = BeautifulSoup(f_content, "lxml")
#print(soup.prettify())
all_torr_soup = html_soup.find(class_='torrents').find(id="form_torrent")
#print(all_torr_soup.prettify())
every_torr_soup = all_torr_soup.find_all( "tr", recursive=False)
every_torr_soup.remove(every_torr_soup[0])
title = []
uploader = []
downloader = []
download_link = []
for i in range(len(every_torr_soup)):
    if not ((every_torr_soup[i].find(class_ = "download")) is None):
        download_link.append("https://pt.keepfrds.com/" + every_torr_soup[i].find(class_ = "download").parent.get("href"))
        downloader.append(int(every_torr_soup[i]("td")[8].string))
        title.append(every_torr_soup[i]("a")[1].attrs['title'])
        uploader.append(int(every_torr_soup[i]("td")[7].string))
    else:
        continue

    
for i in range(len(title)):
    movie_title = re.compile('【(.*)】').findall(title[i])[0]
    if (downloader[i]>40 and uploader[i]<5):
        print("%-10s\n%s\n%-05d  %-05d"%(movie_title,download_link[i],uploader[i],downloader[i]))
