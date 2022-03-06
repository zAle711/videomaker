import re
import requests
from requests_html import AsyncHTMLSession
from setup import DOWNLOAD_FOLDER
import util
from bs4 import BeautifulSoup
import time
import random

class ImageDownloader:
   
    google_link = "https://www.google.com/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
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
        self.current_line = 0
        self.current_urls = "Dio Porco"
    
    
    def getQuery(self, line: str) -> str: 
        """convert line from text file to a valid query

        Args:
            line (str): text file line

        Returns:
            str: valid query
        """
        return re.sub(r"\(.+\)", "", line.split("-")[1]).strip()
   
    async def getPageContent(self, query):
        """Fetch the query, render the page and return html page content

        Args:
            query (str): google search query

        Returns:
            str: page html content
        """
        query_name = util.replaceSpace(query)       
        self.params.update(q=query_name)
        #Request to download page
        session = AsyncHTMLSession()
        session.headers = self.headers
        page_content = await session.get(url=self.google_link, params=self.params)
        #render the page so i can read script text
        await page_content.html.arender()
        #returns html contet after rendering the page
        return page_content.html.html

    def findUrl(self, html_page:str) -> list:
        """This function scrapes the html page to find all urls that lead to images.

        Args:
            html_page (str): html rendered content of google search page

        Returns:
            list: list full of urls
        """
        REGEX_PATTERN = "(https?:\/\/[A-Z,a-z,0-9, -. _, \.,\/]+)(\.)(png|jpg)"
        #util.saveHTML(html_page)
        html = BeautifulSoup(html_page, "html.parser")
        urls_images = None
        for script in html.find_all('script'):
            if "AF_initDataCallback" in str(script):
                urls_images = re.findall(REGEX_PATTERN, str(script))
        #join list of 3 groups matched with regex
        urls = ["".join(url) for url in urls_images]
        return urls

    def saveImage(self, image_name:str, image_url:str) -> None:
        """This function makes a get request to the image_url and saves image named like image_name

        Args:
            image_name (str): name used to save image
            image_url (str): url used to download image
        """
        image_data = requests.get(url=image_url, headers=self.headers).content
        #cant name a file with ? 
        if "?" in image_name:
            image_name = re.sub("\?", "$", image_name)
        with open(DOWNLOAD_FOLDER.joinpath(image_name.strip()+image_url[-4:]), "wb") as image:
            image.write(image_data)
            image.flush()

    async def getAllUrls(self):
        file_line = self.readFileLine()
        if (file_line):
            query = self.getQuery(file_line)
            html_page = await self.getPageContent(query)
            self.current_urls = self.findUrl(html_page)
            print(f"Urls trovati -> {self.current_urls}")
            return self.current_urls


    def getUrls(self):
        return self.current_urls

    def readFileLine(self):
        with open(self.file_name, "r") as fp:
            
            for i,line in enumerate(fp):
                if i == self.current_line:
                    self.current_line += 1
                    return line.strip()
            
            return None
                           
    def downloadAllImage(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                print(f"Downloading images {index+1}/{len(lines)}")
                query = self.getQuery(line)
                html_page = self.getPageContent(query)
                urls = self.findUrl(html_page)
                self.saveImage(image_name=line, image_url=urls[random.randint(0,5)])
                time.sleep(5)

if __name__ == "__main__":
    ImageDownloader().downloadAllImage()