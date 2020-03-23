import requests
from bs4 import BeautifulSoup
import re
from model.news import News
from database import Database

BASE_PATH = 'https://www.infomoney.com.br'
NEWS_PATH = BASE_PATH + '/mercados'


def scrap():
    print('Starting Info Money Scraper...')

    news = []
    hrefs = []
    titles = []
    paragraphs = []

    get_news(hrefs, titles)
    print(hrefs, titles)
    for i in range(0, len(hrefs)):
        get_news_content(hrefs[i], paragraphs)
        news.append(News(titles[i], hrefs[i], paragraphs))
        paragraphs = []

    db = Database()
    for el in news:
        db.save(el)
    print('All news were saved.')


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
            paragraphs.append(sanitize_paragraph(text))

def sanitize_paragraph(paragraph):
    paragraph = paragraph.replace(u'\xa0', u' ')
    return paragraph

def is_not_script_tag(text):
    return text and "<script>" not in text

def is_not_tag(text):
    return text and text[:1] != '<'


if __name__ == "__main__":
    scrap()
