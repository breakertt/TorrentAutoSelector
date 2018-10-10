# -*- coding:utf-8 -*-

import requests
import re
from PIL import Image
import io
import os

pt_link = {
        'frds': 'http://pt.keepfrds.com/',
        'hdchina': 'https://hdchina.org/',
        'u2': '3258'
    }

def get_cookies( username, passwd, pt = "frds"):
    login_url = pt_link[pt] + "login.php"
    takelogin_url = pt_link[pt] + "takelogin.php" # login post url
    my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    sess = requests.Session()
    login_content =sess.get(login_url, headers = my_headers)
    pattern = re.compile(r'imagehash=(.*)" border="0"')
    
    #print(login_content.content)
    
    captcha_hash = pattern.findall(login_content.content.decode('utf-8'))[0]
    
    captcha_url = pt_link[pt] + "image.php?action=regimage&imagehash=" + captcha_hash
    with requests.get(captcha_url) as captcha_img:
        captcha_img_content = io.BytesIO(captcha_img.content)
    Image.open(captcha_img_content).show() # show captcha
    captcha_input = input("Please enter the captcha : ")
    my_data = {
        'username' : username,
        'password' : passwd,
        'imagestring' : captcha_input,
        'imagehash' : captcha_hash,
        'ssl' : 'yes'
    }
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


def loadcookie(pt):
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

if __name__ == "__main__":
    #get_cookies( username='null', passwd='null')
    loadcookie('frds')