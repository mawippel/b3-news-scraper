import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
from model.news import News
from database import Database
import locale
from utils.paragraph_utils import ParagraphUtils
from utils.anchor_utils import AnchorUtils
from utils.log_utils import LogUtils

db = None


def scrap():
    global db
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    db = Database()
    _scrap()


def _scrap():
    LogUtils.start('Info Money')
    news = []
    hrefs, titles = get_news_ignoring_fetched_links(db.get_fetched_links())
    for i in range(len(hrefs)):
        href = hrefs[i]
        title = titles[i]
        paragraphs, publish_date = get_news_content_by_href(href)
        news.append(News(title, href, paragraphs, 'InfoMoney',
                         'https://is2-ssl.mzstatic.com/image/thumb/Purple123/v4/5c/df/a9/5cdfa9b4-913f-8b4d-a99d-1c6f2662061e/AppIcon-0-1x_U007emarketing-0-0-85-220-0-4.png/1200x630wa.png', publish_date))
    db.save_all_news(news)
    LogUtils.end('Info Money', hrefs)


def get_news_ignoring_fetched_links(fetched_links):
    """ Retrieves the latest news and parse its title/href """
    hrefs = []
    titles = []
    soup = read_page_html()

    htmlTitles = soup.findAll('div', {"id": re.compile("^post-")})
    for item in htmlTitles:
        txt_href = get_link(item)
        txt_title = get_title(item)
        if AnchorUtils.is_not_fetched(txt_href, fetched_links):
            hrefs.append(txt_href)
            titles.append(txt_title)
    return hrefs, titles


def get_news_content_by_href(href):
    """ Returns the paragraphs of the article """
    paragraphs = []
    page = requests.get(href)
    soup = BeautifulSoup(page.text, 'html.parser')
    fullContent = soup.findAll('article', {"id": re.compile("^post-")})
    # Get the texts that are outside paragraphs
    for item in fullContent:
        article_paragraphs = item.find_all('p')
        for paragraph in article_paragraphs:
            text = paragraph.getText()
            if ParagraphUtils.is_valid(text):
                text = ParagraphUtils.sanitize(text)
                paragraphs.extend(ParagraphUtils.split(text))

    datetime_object = get_metadata(soup)

    return paragraphs, datetime_object


def get_link(item):
    return item.find('a')['href']


def get_title(item):
    return item.find('a').get('title')


def read_page_html():
    page = requests.get('https://www.infomoney.com.br/mercados')
    return BeautifulSoup(page.text, 'html.parser')


def get_metadata(soup):
    # get publish time
    articleDate = soup.find(class_='entry-date')
    strippedDate = articleDate.get('datetime').strip()
    datetime_object = datetime.strptime(
        strippedDate, '%Y-%m-%dT%H:%M:%S%z')
    return datetime_object


if __name__ == "__main__":
    scrap()
