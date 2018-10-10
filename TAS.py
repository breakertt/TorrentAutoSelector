# -*- coding:utf-8 -*-

import requests
import re
import sys
import os
import bs4
import Cookies

my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
    }
get_cookies
def get_cookies(username, passwd, pt, login=False):
    filename = "cookies_%s.txt"%pt
    if login:
        i = 0
        while (1 == 0):
            i = Cookies.get_cookies( username=username, passwd=passwd, pt = pt)
        cookies = Cookies.loadcookie(pt = pt)  # 读取cookie
        return cookies
    else:
        cookies = Cookies.loadcookie(filename)
        if cookies != 0:
            return cookies
        else:
            print("load cookie false")