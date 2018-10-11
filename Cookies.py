# -*- coding:utf-8 -*-

import requests
import re
from PIL import Image
import io
import os

def get_cookies( username, passwd, ptsite_dict, pt = "frds"):
    login_url = ptsite_dict[pt]['urls']['login']
    takelogin_url = ptsite_dict[pt]['urls']['takelogin'] # login post url

    my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    sess = requests.Session()
    login_content =sess.get(login_url, headers = my_headers)
    pattern = re.compile(ptsite_dict[pt]['captcha_pattern'])
    print(pattern)
    #print(login_content.content)
    #print(login_content.content)
    captcha_hash = pattern.findall(login_content.content.decode('utf-8'))
    print(captcha_hash)
    captcha_url = ptsite_dict[pt]['urls']['captcha'] + captcha_hash[0]
    print(captcha_url)
    with requests.get(captcha_url) as captcha_img:
        captcha_img_content = io.BytesIO(captcha_img.content)
    Image.open(captcha_img_content).show() # show captcha
    captcha_input = input("Please enter the captcha : ")
    my_data = ptsite_dict[pt]['login_data']
    
    my_data['imagestring'] = captcha_input
    my_data['imagehash'] = captcha_hash
    my_data['username'] = username
    my_data['password'] = passwd

    login = sess.post(takelogin_url, headers = my_headers, data = my_data)
    print(login.url, login.status_code, login.history)
    if (login.url.find('index')==-1):
        print("Save cookies failed, Please run again!")
        return 0
    cookies = sess.cookies
    with open("cookies_%s.txt"%pt , 'w') as f:
        f.write('; '.join(['='.join(item) for item in cookies.items()]))
        print('Save cookies successsfully!')
        return 1
    print


def loadcookie( ptsite_dict, pt):
    loadcookies = {}
    filename = "cookies_%s.txt"%pt
    if not os.path.exists(filename):
        print('The cookies file %s doesn\'t exist, Please login again.'%filename)
        return 0
    if os.path.getsize(filename)<10:
        os.remove(filename)
        print('The cookies file %s is empty, Please login again.'%filename)
        return 0
    with open(filename , 'r') as f:
        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            loadcookies[name] = value
    print('Load cookies successsfully!')
    return loadcookies

#if __name__ == "__main__":
    #get_cookies( username='breakertt', passwd='xsgty1999118xyz')
    #loadcookie('frds')
    