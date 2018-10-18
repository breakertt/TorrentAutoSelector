import re

from bs4 import BeautifulSoup


def myInt(str):
    return int(re.sub('[^0-9]','', str))

def GetTorrInfo(torr_html, pt, ptsite_dict):

    html_soup = BeautifulSoup(torr_html, "lxml")
    torr_list = []
    title = []
    uploader = []
    downloader = []
    download_link = []
    print("")

    if pt == "frds":
        all_torr_soup = html_soup.find(id = "form_torrent")
        #print(all_torr_soup.prettify())
        every_torr_soup = all_torr_soup.find_all( "tr", recursive=False)
        every_torr_soup.remove(every_torr_soup[0])
        for i in range(len(every_torr_soup)):
            if not ((every_torr_soup[i].find(class_ = "download")) is None):
                download_link.append(ptsite_dict[pt]['urls']['link'] + every_torr_soup[i].find(class_ = "download").parent.get("href"))
                downloader.append(myInt(every_torr_soup[i]("td")[8].string))
                title.append(every_torr_soup[i]("a")[1].attrs['title'])
                uploader.append(myInt(every_torr_soup[i]("td")[7].string))
            else:
                continue

    if pt == "hdc":
        every_torr_soup = html_soup.find(class_ = "torrent_list")("tr", recursive=False)
        every_torr_soup.remove(every_torr_soup[0])
        for i in range(len(every_torr_soup)):
            if not ((every_torr_soup[i].find(class_ = "download")) is None):
                download_link.append(ptsite_dict[pt]['urls']['link'] + every_torr_soup[i].find(class_ = "download").parent.get("href"))
                downloader.append(myInt(every_torr_soup[i].find(class_ = "t_leech").string))
                title.append(every_torr_soup[i].find("h3").string)
                uploader.append(myInt(every_torr_soup[i].find(class_ = "t_torrents").string))
            else:
                continue

    if pt == "ttg":
        every_torr_soup = html_soup.find_all(class_ = re.compile("hover_hr"))
        for i in range(len(every_torr_soup)):
            if not ((every_torr_soup[i].find(class_ = "dl_a")) is None):
                download_link.append(ptsite_dict[pt]['urls']['link'] + every_torr_soup[i].find(class_ = "dl_a").get("href"))
                downloader.append(myInt(every_torr_soup[i]("td")[8].get_text().split("/\n")[1]))
                title_len = len(every_torr_soup[i].find(class_ = "name_left")("b"))
                title.append(every_torr_soup[i].find(class_ = "name_left")("b")[title_len-1].get_text())
                uploader.append(myInt(every_torr_soup[i]("td")[8].get_text().split("/\n")[0]))
            else:
                continue

    if pt == "hdh":
        all_torr_soup = html_soup.find(id="torrenttable")
        #print(all_torr_soup.prettify())
        every_torr_soup = all_torr_soup.find_all( "tr", recursive=False)
        every_torr_soup.remove(every_torr_soup[0])
        for i in range(len(every_torr_soup)):
            if not ((every_torr_soup[i].find(class_ = "download")) is None):
                download_link.append(ptsite_dict[pt]['urls']['link'] + every_torr_soup[i].find(class_ = "download").parent.get("href"))
                downloader.append(myInt(every_torr_soup[i]("td")[11].string))
                title.append(every_torr_soup[i]("a")[1].attrs['title'])
                uploader.append(myInt(every_torr_soup[i]("td")[10].string))
            else:
                continue

    if pt == "opcd":
        all_torr_soup = html_soup.find(class_="torrents")
        #print(all_torr_soup.prettify())
        every_torr_soup = all_torr_soup.find_all( "tr", recursive=False)
        every_torr_soup.remove(every_torr_soup[0])
        for i in range(len(every_torr_soup)):
            if not ((every_torr_soup[i].find(class_ = "download")) is None):
                download_link.append(ptsite_dict[pt]['urls']['link'] + every_torr_soup[i].find(class_ = "download").parent.get("href"))
                downloader.append(myInt(every_torr_soup[i]("td")[11].string))
                title.append(every_torr_soup[i]("a")[1].attrs['title'])
                uploader.append(myInt(every_torr_soup[i]("td")[10].string))
            else:
                continue
                
    if pt == "cmct":
        all_torr_soup = html_soup.find(class_="torrents")
        #print(all_torr_soup.prettify())
        every_torr_soup = all_torr_soup.find_all( "tr", recursive=False)
        every_torr_soup.remove(every_torr_soup[0])
        for i in range(len(every_torr_soup)):
            if not ((every_torr_soup[i].find(class_ = "download")) is None):
                download_link.append(ptsite_dict[pt]['urls']['link'] + every_torr_soup[i].find(class_ = "download").parent.get("href"))
                downloader.append(myInt(every_torr_soup[i]("td")[8].string))
                title.append(every_torr_soup[i]("a")[1].attrs['title'])
                uploader.append(myInt(every_torr_soup[i]("td")[7].string))
            else:
                continue
                
    
    #print selected torrents
    for i in range(len(title)):
        movie_title = title[i]
        #print("%-10s\n%s\n%-05d  %-05d"%(movie_title,download_link[i],uploader[i],downloader[i]))
        if (downloader[i]>40 and uploader[i]<5):
            torr_list.append([pt,movie_title,download_link[i],uploader[i],downloader[i]])
    if len(torr_list)==0:
        print("No Torrent has been Selected.")
    else:
        print("Selected Torrents:")
    for torr in torr_list:
        print("%-10s\n%s\n%-05d  %-05d"%(torr[1],torr[2],torr[3],torr[4]))
    return torr_list
