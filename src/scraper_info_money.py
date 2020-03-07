import requests
from bs4 import BeautifulSoup
import re

BASE_PATH = 'https://www.infomoney.com.br'
NEWS_PATH = BASE_PATH + '/mercados'


def scrap():
    print('Starting Info Money Scraper...')

    hrefs = []
    titles = []
    paragraphs = []

    get_news(hrefs, titles)
    print(hrefs, titles)
    # for title in titles:
    #     news_path = BASE_PATH + title
    #     get_news_content(news_path, paragraphs)
    news_path = BASE_PATH + '/negocios/coronavirus-faz-empresas-perderem-bilhoes-em-valor-de-mercado-por-reducao-de-previsao-de-lucro/'
    get_news_content(news_path, paragraphs)
    print(paragraphs)


def get_news(hrefs, titles):
    """ Retrieves the latest news and parse its title/href """
    page = requests.get(NEWS_PATH)
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.findAll('div', {"id":re.compile("^post-")})
    for item in htmlTitles:
        txt_href = item.find('a')['href']
        txt_title = item.find('a').get('title')
        hrefs.append(txt_href)
        titles.append(txt_title)


def get_news_content(news_path, paragraphs):
    """ Returns the paragraphs of the article """
    page = requests.get(news_path)
    soup = BeautifulSoup(page.text, 'lxml')
    fullContent = soup.findAll('article', {"id":re.compile("^post-")})
    # Get the texts that are outside paragraphs
    for item in fullContent:
        article_paragraphs = item.find_all('p')
        for paragraph in article_paragraphs:
            text = paragraph.getText()
            paragraphs.append(text)

def is_not_script_tag(text):
    return text and "<script>" not in text

def is_not_tag(text):
    return text and text[:1] != '<'


if __name__ == "__main__":
    scrap()
