# -*- coding:utf-8 -*-

import io
import os
import re

import requests
from PIL import Image


def get_cookies( username, passwd, ptsite_dict, pt = "frds"):

    #load essential values
    loginUrl = ptsite_dict[pt]['urls']['login']
    takeloginUrl = ptsite_dict[pt]['urls']['takelogin'] # login post url
    myHeaders = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    #start session
    sess = requests.Session()
    login_content =sess.get(loginUrl, headers = myHeaders)

    #load login data
    myData = ptsite_dict[pt]['login_data']
    myData['username'] = username
    myData['password'] = passwd

    #get captcha info and require user to enter
    if ptsite_dict[pt]['captcha']['exist'] == 'True':
        pattern = re.compile(ptsite_dict[pt]['captcha']['pattern'])
        #get the url of captcha
        captchaHash = pattern.findall(login_content.content.decode('utf-8'))
        captchaUrl = ptsite_dict[pt]['urls']['captcha'] + captchaHash[0]
        print("Captcha URL = %s"%captchaUrl)
        #download captcha image and show
        with requests.get(captchaUrl) as captchaImg:
            captchaImgContent = io.BytesIO(captchaImg.content)
            Image.open(captchaImgContent).show()
        #input captcha
        captchaInput = input("Please enter the captcha : ")
        #save captcha infos into post data
        myData['imagestring'] = captchaInput
        if 'imagehash' in myData:
            myData['imagehash'] = captchaHash

    #try login
    login = sess.post(takeloginUrl, headers = myHeaders, data = myData)
    print(login.url, login.status_code, login.history)

    #check login status
    if (login.url.find('index')==-1) and ((login.url.find('my.php')==-1)):
        print("Save cookies failed, Please run again!")
        return 0

    #get cookies (I debugged for a thousand years in this line Fxxk!)
    cookies = sess.cookies

    #save cookies
    with open("cookies_%s.txt"%pt , 'w') as f:
        f.write('; '.join(['='.join(item) for item in cookies.items()]))
        print('Save cookies successsfully!')
        return 1

def loadcookie( ptsite_dict, pt):
    
    # load essential values
    loadcookies = {}
    filename = "cookies_%s.txt"%pt

    # check cookies file
    if not os.path.exists(filename):
        print('The cookies file %s doesn\'t exist, Please login again.'%filename)
        return 0
    elif os.path.getsize(filename)<10:
        os.remove(filename)
        print('The cookies file %s is empty, Please login again.'%filename)
        return 0

    # load cookies
    with open(filename , 'r') as f:
        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            loadcookies[name] = value
    print('Load cookies successsfully!')
    return loadcookies
