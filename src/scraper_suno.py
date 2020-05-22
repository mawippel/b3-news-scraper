import requests
import pytz
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from model.news import News
from database import Database
import locale
from utils.paragraph_utils import ParagraphUtils
from utils.anchor_utils import AnchorUtils
from utils.log_utils import LogUtils

db = None


def scrap():
    global db
    db = Database()
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    _scrap()


def _scrap():
    LogUtils.start('Suno')
    news = []
    hrefs, titles = get_news_ignoring_fetched_links(db.get_fetched_links())
    for i in range(len(hrefs)):
        href = hrefs[i]
        title = titles[i]
        paragraphs, publish_date = get_news_content_by_href(href)
        news.append(News(title, href, paragraphs, 'Suno Notícias',
                         'https://www.sunoresearch.com.br/wp-content/uploads/2019/12/suno-research.jpg', publish_date))
    db.save_all_news(news)
    LogUtils.end('Suno', hrefs)


def get_news_ignoring_fetched_links(fetched_links):
    hrefs = []
    titles = []

    page = requests.get('https://www.sunoresearch.com.br/noticias/mercado/')
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.find_all(class_='list-item')
    for item in htmlTitles:
        title = item.find('h3', {'class': 'post__title'})
        txt_href = title.find('a')['href']
        txt_title = title.find('a').text
        if AnchorUtils.is_not_fetched(txt_href, fetched_links):
            hrefs.append(txt_href)
            titles.append(txt_title)
    return hrefs, titles


def get_news_content_by_href(href):
    """ Returns the paragraphs of the article """
    paragraphs = []
    page = requests.get(href)
    soup = BeautifulSoup(page.text, 'html.parser')
    fullContent = soup.find('div', itemprop="articleBody")
    # Get the texts that are outside paragraphs
    article_paragraphs = fullContent.find_all('p', recursive=False)
    for paragraph in article_paragraphs:
        text = paragraph.getText()
        if ParagraphUtils.is_valid(text):
            text = ParagraphUtils.sanitize(text)
            paragraphs.extend(ParagraphUtils.split(text))

    # get publish time
    articleDate = soup.find(class_='time')
    strippedDate = articleDate.get('datetime').strip()
    datetime_object = datetime.strptime(
        strippedDate, '%Y-%m-%dT%H:%M:%S%z')
    datetime_object += timedelta(hours=3)
    tz = pytz.timezone('America/Sao_Paulo')
    datetime_object = datetime_object.replace(tzinfo=pytz.utc).astimezone(tz)
    return paragraphs, datetime_object


if __name__ == "__main__":
    scrap()
