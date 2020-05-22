import locale
import pytz
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from model.news import News
from database import Database
from utils.paragraph_utils import ParagraphUtils
from utils.anchor_utils import AnchorUtils
from utils.log_utils import LogUtils
import re

db = None


def scrap():
    global db
    db = Database()
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    _scrap()


def _scrap():
    LogUtils.start('Exame')
    hrefs, titles = get_news_ignoring_fetched_links(db.get_fetched_links())
    news = []
    for i in range(len(hrefs)):
        href = hrefs[i]
        title = titles[i]
        paragraphs, publish_date = get_news_content_by_href(href)
        news.append(News(title, href, paragraphs, 'EXAME Notícias',
                         'https://abrilexame.files.wordpress.com/2019/08/logo-exame.png?w=150', publish_date))
    db.save_all_news(news)
    LogUtils.end('Exame', hrefs)


def get_news_ignoring_fetched_links(fetched_links):
    hrefs = []
    titles = []
    page = requests.get('https://exame.abril.com.br/noticias-sobre/acoes/')
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.findAll('li', {"id": re.compile("^post-")})
    for item in htmlTitles:
        txt_href = item.find('a')['href']
        txt_title = item.find('a').get('title')
        if AnchorUtils.is_not_fetched(txt_href, fetched_links):
            if AnchorUtils.is_valid(txt_href):
                hrefs.append(txt_href)
                titles.append(txt_title)
    return hrefs, titles


def get_news_content_by_href(href):
    paragraphs = []
    page = requests.get(href)
    soup = BeautifulSoup(page.text, 'html.parser')
    fullContent = soup.find(class_='article-content')

    # Get the texts that are outside paragraphs
    for without_paragraph_text in fullContent:
        text = str(without_paragraph_text).strip()
        # Ignore tags inside the text, in case it happens
        if ParagraphUtils.is_valid(text):
            text = ParagraphUtils.sanitize(text)
            paragraphs.extend(ParagraphUtils.split(text))
    fullContent = fullContent.find_all('p', recursive=False)

    # Get the texts that are inside paragraphs
    for i in range(0, len(fullContent) - 1):
        text = fullContent[i].getText()
        if ParagraphUtils.is_valid(text):
            text = ParagraphUtils.sanitize(text)
            paragraphs.extend(ParagraphUtils.split(text))

    # Get publish date
    articleDate = soup.find(class_='article-date')
    date = articleDate.find('span').getText()
    sanitized_date = sanitize_date(date)

    try:
        datetime_object = datetime.strptime(
            sanitized_date, '%d/%m/%Y às %Hh%M')
    except Exception as e:
        datetime_object = datetime.strptime(
            sanitized_date, '%d %b %Y às %Hh%M')
    tzbr = pytz.timezone(
        'America/Sao_Paulo').localize(datetime_object).astimezone(pytz.UTC)
    return paragraphs, tzbr


def sanitize_date(date):
    # Remover o "Publicado em:"
    auxDate = date.replace("Publicado em:", "")
    # Remover o que vier depois do primeiro hífen
    auxDate = auxDate.split('-')[0]
    auxDate = auxDate.strip()
    return auxDate


if __name__ == "__main__":
    scrap()
