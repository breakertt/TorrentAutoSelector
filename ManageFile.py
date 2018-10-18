# -*- coding:utf-8 -*-

import datetime
import os
import shutil
import sys
import time

import requests
from lxml import etree


def load_xml(path):
    parser = etree.XMLParser(encoding="utf-8", strip_cdata=False, remove_blank_text=True)
    root = etree.parse(path, parser=parser)
    return root

def get_item(torrTitle, torrFilename):
    item = etree.Element('item')
    item.text = None
    title = etree.Element('title')
    title.text = torrTitle
    item.append(title)
    enclosure = etree.Element('enclosure')
    enclosure.set('url','http://127.0.0.1:4573/%s' % torrFilename)
    enclosure.set('type','application/x-bittorrent')
    item.append(enclosure)
    return item

def checkFiles():
    #check folder
    #get new dir
    web_dir = os.path.join(os.path.dirname(__file__), 'public')
    if not os.path.exists(web_dir):
        os.makedirs(web_dir)
    os.chdir(web_dir)
    if not os.path.exists("expire"):
        os.makedirs("expire")
    #check rss.xml
    if not os.path.isfile("torrentrss.xml"):
        print("torrentrss.xml does't exist, try downloadling")
        torrentrss = requests.get("https://raw.githubusercontent.com/imaginebreake/TorrentAutoSelector/master/public/torrentrss.xml")
        print("Download success, Time = %ds"%round(torrentrss.elapsed.microseconds / 100000))
        with open("torrentrss.xml", "wb") as savefile:
            for data in torrentrss.iter_content():
                savefile.write(data)

def AddTorrToRss(rssList):
    xmlPath = "public/torrentrss.xml"
    root = load_xml(xmlPath)
    parent = root.xpath("channel")[0]
    for torr in rssList:
        node = get_item(torrTitle = torr[0], torrFilename = torr[1])
        parent.append(node)
    root.write(xmlPath, pretty_print=True, xml_declaration=True, encoding='utf-8')

def GetFileTime(filePath):
    t1 = os.path.getctime(filePath)
    t2 = os.path.getmtime(filePath)
    if t1 < t2:
        return t1
    else:
        return t2

def DeteInRss(fileList):
    xmlPath = "torrentrss.xml"
    root = load_xml(xmlPath)
    links = root.xpath("//enclosure")
    for link in links:
        url = link.get('url', '')
        for file in fileList:
            if url.find(file[0]) != -1:
                parentnode = link.getparent()
                parentnode.getparent().remove(parentnode)
    root.write(xmlPath, pretty_print=True, xml_declaration=True, encoding='utf-8')

def MoveFile(fileList):
    for file in fileList:
        print("Moving %s" % file[0])
        print("This file existed for %d hours." % file[1])
        shutil.move(file[0], "expire/%s" % file[0])

def DeleteExipredTorr():
    fileList = []
    web_dir = os.path.join(os.path.dirname(__file__), 'public')
    os.chdir(web_dir)
    nowTime = time.time()
    for fileName in os.listdir(web_dir):
        if os.path.splitext(fileName)[1] == '.torrent':
            fileTime = GetFileTime(fileName)
            DeltaTime = round((nowTime - fileTime) / 3600)
            if DeltaTime >= 8:
                fileList.append([fileName,DeltaTime])
    MoveFile(fileList)
    DeteInRss(fileList)
