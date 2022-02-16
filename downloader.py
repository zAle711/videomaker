import re
import requests
from requests_html import HTMLSession
from setup import DOWNLOAD_FOLDER
import util
from bs4 import BeautifulSoup

class ImageDownloader:
   
    google_link = "https://www.google.com/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    params = {
        "q": "",
        "tbm": "isch",
    }

    def __init__(self, file_name = "text.txt") -> None:
        self.file_name = file_name

    def getQuery(self, line):
        return re.sub(r"\(.+\)", "", line).strip()
        
    def downloadImage(self, image_name):
        query_name = util.replaceSpace(image_name)       
        self.params.update(q=query_name)
        #Request to download page
        session = HTMLSession()
        session.headers = self.headers
        page_content = session.get(url=self.google_link, params=self.params)
        #render the page so i can read script text
        page_content.html.render()
        
        #Scrape page to find image url
        image_url = self.findUrl(page_content.html.html)
        self.saveImage(image_name, image_url)
   
    def saveImage(self, image_name, image_url):
        image_data = requests.get(url=image_url, headers=self.headers).content
        with open(DOWNLOAD_FOLDER.joinpath(image_name.rstrip()+image_url[-4:]), "wb") as image:
            image.write(image_data)
            image.flush()
   
    def findUrl(self, html_page):
        REGEX_PATTERN = "https?:\/\/[A-Z,a-z,0-9, -. _, \.,\/]+\.jpg|jpeg|png"
        #util.saveHTML(html_page)
        html = BeautifulSoup(html_page, "html.parser")
        urls_images = None
        for script in html.find_all('script'):
            if "AF_initDataCallback" in str(script):
                urls_images = re.findall(REGEX_PATTERN, str(script))
        return urls_images[0]           
    
    def downloadAllImage(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                query = self.getQuery(line)
                self.downloadImage(query)


if __name__ == "__main__":
    ImageDownloader().downloadAllImage()