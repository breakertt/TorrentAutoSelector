# -*- coding:utf-8 -*-

import requests
import re
import sys
import os
from bs4 import BeautifulSoup
import Cookies
import json


my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
    }

def get_cookies(username = '123', passwd = '', pt = '', login=False):
    filename = "cookies_%s.txt"%pt
    if login:
        i = 0
        while (i == 0):
            i = Cookies.get_cookies( username=username, passwd=passwd, pt = pt, ptsite_dict = ptsite_dict)
        cookies = Cookies.loadcookie(pt = pt, ptsite_dict = ptsite_dict)  # 读取cookie
        return cookies
    else:
        cookies = Cookies.loadcookie(pt = pt, ptsite_dict = ptsite_dict)
        if cookies != 0:
            return cookies
        else:
            print("load cookie false")

with open("ptsite_info.json",'r') as load_f:
    ptsite_dict = json.load(load_f)
    #print(ptsite_dict)
i = ""
for pt in ptsite_dict:
    i += pt + " "
pt = input("Please choose the ptsite (supported pt site : %s) : " % i)

# load cookies
cookies = get_cookies( username='null', passwd='null', pt=pt, login=True)
sess = requests.session()
torr_url = ptsite_dict[pt]['urls']['torrent']
print("Staring Loading Page URL = \"%s\""%torr_url)
torr_get = sess.get( torr_url, headers=my_headers, cookies = cookies )
print("Page loaded, Time = %ds"%round(torr_get.elapsed.microseconds / 100000))
print("Url = \"%s\" Status_code = %s"%(torr_get.url, torr_get.status_code))



# find hot torrent


html_soup = BeautifulSoup(torr_get.content, "lxml")
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

