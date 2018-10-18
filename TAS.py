# -*- coding:utf-8 -*-

import requests
import re
import sys
import os
import Cookies
import json
import GetTorrInfo
import getopt
import datetime
import http.server
import socketserver
import ManageFile
from bs4 import BeautifulSoup
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import unquote

#load essential values
login = False
pt_choosen = []
myHeaders = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
    } 
with open("ptsite_info.json",'r') as load_f:
    ptsite_dict = json.load(load_f)

def httpserver():
    PORT = 4573
    web_dir = os.path.join(os.path.dirname(__file__), 'public')
    os.chdir(web_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("\n\n\nPLEASE DO NOT OPEN THIS IN CHROME, MAY LEAD TO CRASH OF HTTP-SERVER!!!\n\n\n")
    print("Rss Url : http://127.0.0.1:4573/torrentrss.xml")
    print("Serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

def get_cookies(username = '123', passwd = '', pt = '', login=False):
    #select get_cookies mod
    if login:
        i = 0
        tryTimes = 0
        while (i == 0):
            #let user re-enter the username and passwd
            if tryTimes != 0:
                username = input("Enter your username : ")
                passwd = input("Enter your password : ")
            i = Cookies.get_cookies( username=username, passwd=passwd, pt = pt, ptsite_dict = ptsite_dict)
            tryTimes += 1
        cookies = Cookies.loadcookie(pt = pt, ptsite_dict = ptsite_dict)  # 读取cookie
    else:
        cookies = Cookies.loadcookie(pt = pt, ptsite_dict = ptsite_dict)
        # if load cookies failed
        if cookies == 0:
            print("Cookies load failed, try relogin?")
            if input("if yes, enter 1\n") == "1":
                username = input("Enter your username : ")
                passwd = input("Enter your password : ")
                cookies = get_cookies( username=username, passwd=passwd, pt=pt, login=True)
                return cookies
            else:
                print("wtf??? you dont want to relogin??? bye bye")
                os._exit(0)
    return cookies                

def get_torrhtml(pt, cookies, ptsite_dict):
    torr_url = ptsite_dict[pt]['urls']['torrent']
    print("Staring Loading Page URL = \"%s\""%torr_url)
    code = 502 # a initial fail code
    tryTimes = 0
    loadFlag = True
    # load page
    while (code != 200 and tryTimes < 5):
        torr_get = requests.get(torr_url, headers=myHeaders, cookies = cookies, timeout=(10,10))
        print("Page loaded, Time = %ds"%round(torr_get.elapsed.microseconds / 100000))
        print("Url = \"%s\" Status_code = %s"%(torr_get.url, torr_get.status_code))
        code = torr_get.status_code
        tryTimes += 1
    if tryTimes>=5:
        loadFlag = False
    return (torr_get, loadFlag)

def get_torrents(pt, cookies, torr_list):
    print("\nDownloading torrents")
    rssList = []
    for torr in torr_list:
        try:
            #try download torrent
            torr_file = requests.get(torr[2], headers=myHeaders, cookies = cookies, timeout=(5, 20))
            #get filename
            filename_pattern = re.compile(ptsite_dict[pt]['torr_fn_pattern'])
            filename = filename_pattern.findall(torr_file.headers['content-disposition'])[0]
            filename = unquote(filename)
            print(filename)
            print("Download success, Time = %ds"%round(torr_file.elapsed.microseconds / 100000))
            torr_file_path = "public/%s"%filename
            if not os.path.exists(torr_file_path):
                rssList.append([torr[1],filename])
                with open(torr_file_path, "wb") as savefile:
                    for data in torr_file.iter_content():
                        savefile.write(data)
        except:
            #skip this torrent if error
            print("%s\nSkipped"%torr)
            continue
    return rssList

def analyze_pt(pt_choosen,ptsite_dict):
    print("")

    #print time
    print("Now Time : "+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #analyze each ptsite
    for pt in pt_choosen:

        try:
            print("\nStarting Analyzing %s"%ptsite_dict[pt]["fullname"])

            #load cookies
            cookies = get_cookies(pt = pt)

            #get torrent.php content
            (torr_get,loadFlag) = get_torrhtml(pt = pt, cookies = cookies, ptsite_dict = ptsite_dict)

            #find hot torrent
            if loadFlag == True:
                #get the list of hot torrents
                torr_list = GetTorrInfo.GetTorrInfo(torr_get.content, pt, ptsite_dict)
                #download torrents
                if len(torr_list)>0:
                    rssList = get_torrents(pt, cookies, torr_list)
                    ManageFile.AddTorrToRss(rssList)
            elif loadFlag == False:
                print("Page Load Failed, this ptsite skipped!/nRelogin is recommended.")
                #if input("if you want to remove the cookies saved file, enter 1\n") == "1":
                #    os.remove("cookies_%s.txt"%pt)
                continue
                
        except Exception as e: 
            print(e)
            continue

if __name__ == "__main__":
    help_msg = """                                                                                      
,@@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@       
,@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@        
,@@@@/          @@@@           ,@@@@/                     
,@@@@/           @@@@          ,@@@@/                     
,@@@@/           @@@@          ,@@@@/                     
,@@@@/           @@@@          ,@@@@/                     
,@@@@/           @@@@          ,@@@@/                     
,@@@@/          @@@@           ,@@@@/                     
,@@@@@@@@@@@@@@@@@@            ,@@@@/                     
,@@@@@@@@@@@@@@@&@             ,@@@@/                                        
,@@@@/                         ,@@@@/                     
,@@@@/                         ,@@@@/                                       
,@@@@/                         ,@@@@/                     
,@@@@/                         .@@@@/                     
,@@@@/                         ,@@@@/                     
,@@@@/                         .@@@@/
\n\nTAS.py -l <login> -p <ptsite>\n
Now support ['hdc', 'frds', 'ttg']
        """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrtam:i:l:p:",
                                   ["help", "login", "ptsite"])
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "help"):
            print(help_msg)
            sys.exit()
        elif opt in ("-l", "--login"):
            login = True
        elif opt in ("-p", "--ptsite"):
            pt_choosen.append(arg)
    print(pt_choosen)

    Process_httpserver = Process(target = httpserver)
    try:
        Process_httpserver.start()
        scheduler = BackgroundScheduler()
        scheduler.add_job(analyze_pt, 'interval', minutes = 15, args=[pt_choosen,ptsite_dict], next_run_time=datetime.datetime.now())
        scheduler.start()
    except KeyboardInterrupt:
        print("Program Ended")
        os._exit(0)
    #analyze_pt(pt_choosen,ptsite_dict)