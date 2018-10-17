# -*- coding:utf-8 -*-

import os
import sys
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
    if not os.path.exists("public"):
        os.makedirs("public")
    #get new dir
    web_dir = os.path.join(os.path.dirname(__file__), 'public')
    os.chdir(web_dir)
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
    
