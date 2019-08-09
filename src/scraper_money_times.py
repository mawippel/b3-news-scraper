import requests
from bs4 import BeautifulSoup

NEWS_PATH = 'https://moneytimes.com.br/ultimas-noticias/'

def scrap():
    print('Starting Money Times scraper...')

    hrefs = []
    titles = []
    paragraphs = []

    get_news(hrefs, titles)

def get_news(hrefs, titles):
    """ Retrieves the latest news and parse its title/href """
    page = requests.get(NEWS_PATH)
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.find_all(id='mais-lidas')
    for item in htmlTitles:
        print(item)

if __name__ == "__main__":
    scrap()