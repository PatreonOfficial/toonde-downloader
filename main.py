#toonde.com downloader
#by PatreonOfficial on github
#v1.1
#15.05.2025
#####################################

#----- Settings -----
saveAsPdf = False       #not implemented
downloadPreview = False



from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import os
import time
from math import floor
from bs4 import BeautifulSoup



#------ URLS
url = input("toomics.com url of Manga: ")
downloadPath = "/home/justus/Pictures/toomics"


#----- Fetch all the Chapters ------
options = Options()
options.add_argument("-headless")
def getChapters(url):
    switch = False
    # ------ Selenium Firefox
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        time.sleep(1)
        source = driver.page_source

    soup = BeautifulSoup(source  , 'html.parser')
    mangaTitle = soup.find_all('div', attrs={'class': 'post-title'})[0].contents[3].contents
    mangaTitle = str(mangaTitle[0]).translate(dict.fromkeys(map(ord, '\n\t'), None))[0:-20]
    # ----- Create Folders
    try:
        os.makedirs(f"{downloadPath}/{mangaTitle}")
    except:
        print()

    collection = soup.find_all('ul', attrs={'class': "sub-chap-list"})

    numOfChapers = 0
    for a in collection:
        for b in a:
            numOfChapers += 1
    numOfChapers = floor((numOfChapers)/2)

    for div in collection:
        for char in div:
            if(switch):
                name = str(char.a.contents[0]).translate(dict.fromkeys(map(ord, '\n\t'), None))
                link = char.a["href"]
                currentChapter = name.split(" - ")
                if(currentChapter[0] != "Vorschau"):
                    print(f"Downloading Chapter {currentChapter[0]}/{numOfChapers} of {currentChapter[1]}")
                    getImageLinks(link, name, mangaTitle)
                elif(downloadPreview):
                    print(f"Downloading Chapter {currentChapter[0]}/{numOfChapers} of {currentChapter[1]}")
                    getImageLinks(link, name, mangaTitle)
                switch = False
            else: switch = True


#------ Download all the Images ------
def download(link, chapter, title):
    img_data = requests.get(link).content
    imgName = link.split("/")[-1]
    try:
        os.mkdir(f'{downloadPath}/{title}/{chapter}')
    except: pass

    with open(f'{downloadPath}/{title}/{chapter}/{chapter} - {imgName}', 'wb') as handler:
        handler.write(img_data)


#----- Fetch All The Image Links ------
def getImageLinks(url, chapter, title):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    collection = soup.find_all('div', attrs={'class': 'page-break no-gaps'})
    for div in collection:
        download(div.contents[1]["data-src"],chapter, title)



getChapters(url)