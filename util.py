import re
from setup import TEST_FOLDER

def saveHTML(html_content):
    with open(TEST_FOLDER.joinpath('downloadedPage.html'), "w", encoding="utf-8") as file:
        file.write(html_content)
        file.flush()

def replaceSpace(name):
    return re.sub(' ', '+', name)