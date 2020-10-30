'''
# import things
# grab download file
# open with code i have
# add to Portfolio class
from requests_html import HTMLSession, HTML, AsyncHTMLSession
# import pandas as pd
# import csv


# async def main(r):
#     return(r.html.arender(reload=False))

# asession = AsyncHTMLSession()
# r = asession.get('http://python-requests.org/')
# main(r)


session = HTMLSession()
r = session.get('http://python-requests.org/')
r.html.render()



# with open("simple.html") as html_file:
#     source = html_file.read()
#     html = HTML(html=source)
#     html.render(retries=20, sleep=3)

# match = html.find('#footer', first=True)
# print(match.html)




'''
session = HTMLSession()

webaddress = "https://www.ishares.com/uk/individual/en/products/etf-investments"



for l in links_list:
    if "filetype" in l:
        print("yay")

data = pd.read_csv(webaddress, header=2, decimal=',')
data.head(3)

main_webaddress = "https://www.ishares.com/uk/individual/en/products/251911/"

filename = 'C:/Users/eocli/Documents/Personal/code/python/mess_files/INRG_holdings.csv'
import csv
with open(filename, newline='') as f:
    r = csv.reader(f)
    for l in r:
        if not l:
            l = 'blank'
        print(l)

print(f)

df = pd.read_csv(f)
r = session.get(main_webaddress)

r.href

links_list = list(r.html.links)
links_list

skiprows = 6

main_data = pd.read_csv(main_webaddress, header=6, decimal=',',
                        skip_blank_lines=True)
'''

# get csv from website directly
import requests
import shutil

def callme(url=main_webaddress):
    r = requests.get(url, verify=False, stream=True)
    if r.status_code!=200:
        print("Failure!")
        exit()
    else:
        r.raw.decode_content = True
        with open("file1.csv", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print("Success!")

if __name__ == '__main__':
    callme()
'''

'''
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib2



# from website
source = requests.get("https://www.ishares.com/uk/individual/en/products/251714/ishares-tips-ucits-etf")
soup = BeautifulSoup(source.content, 'html.parser')
print(soup.title.text)
'''

# from website with js
from bs4 import BeautifulSoup
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main(url):
    page = Page(url)
    soup = BeautifulSoup(page.html, 'html.parser')
    csv_finding = soup.find('p', class_='icon-xls-export')
    print(csv_finding)

# https://www.youtube.com/watch?v=FSH77vnOGqU
# https://stackoverflow.com/questions/42147601/pyqt4-to-pyqt5-mainframe-deprecated-need-fix-to-load-web-pages

main_webaddress = "https://www.ishares.com/uk/individual/en/products/251911/"

if __name__ == '__main__':
    #main(url='https://pythonprogramming.net/parsememcparseface/')
    main(url=main_webaddress)

'''
# just a doc
# os.chdir('C:/Users/eocli/Documents/Personal/code/python/mess_files')
# soup = BeautifulSoup(html_doc, 'html.parser')

# source = requests.get("https://www.ishares.com/uk/individual/en/products/251911/")
html_link = "https://www.ishares.com/uk/individual/en/products/251714/ishares-tips-ucits-etf"

html_info = urllib2.urlopen(html_link)

soup = BeautifulSoup(html_info.read())

with open('example_file_html.txt', 'w') as f:
    for line in soup.prettify():
        f.write(str(line))

soup.title



listy = []
for link in soup.find_all('a', href=True):
    # print(f"/nURL: {link['href']}")
    listy.append(link['href'])

for i in listy:
    if "csv" in i:
        print(i)

'''