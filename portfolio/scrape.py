
import requests
from bs4 import BeautifulSoup


def scrape_for_info(url):
    '''

    Examples
    --------
    >>> from portfolio.scrape import scrape_for_info
    >>> url = "https://www.ishares.com/uk/individual/en/products/253743/"
    >>> soup = scrape_for_info(url)

    '''
    source = requests.get(url, verify=False, stream=True)
    if source.status_code!=200:
        print("Scrape Failure")
        exit()
    else:
        # read
        soup = BeautifulSoup(source.content, 'html.parser')
    
    return soup

def parse_for(soup, looking_for="P/E Ratio"):
    '''
    
    Examples
    --------
    >>> from portfolio.scrape import scrape_for_info, parse_for
    >>> url = "https://www.ishares.com/uk/individual/en/products/253743/"
    >>> soup = scrape_for_info(url)
    >>> parse_for(soup, "P/E Ratio")


    '''

    pass

spans = soup.find_all("span")

for s in spans:
    t = s.get('class')
    print(t)
    if "data" in t:
        print(t)

with open('example_file_html.txt', 'w', encoding='utf-8') as f:
    for line in soup.prettify():
        f.write(str(line))
