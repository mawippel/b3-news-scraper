import requests
from bs4 import BeautifulSoup
from model.news import News
from database import Database
import re

NEWS_PATH = 'https://exame.abril.com.br/noticias-sobre/acoes/'


def scrap():
    print('Starting Exame Scraper...')
    db = Database()

    news = []
    hrefs = []
    titles = []
    paragraphs = []

    fetched_links = db.get_links()

    get_news(hrefs, titles, fetched_links)
    print(hrefs, titles)
    for i in range(0, len(hrefs)):
        get_news_content(hrefs[i], paragraphs)
        news.append(News(titles[i], hrefs[i], paragraphs))
        paragraphs = []

    for el in news:
        db.save(el)
    print('All news were saved.')


def get_news(hrefs, titles, fetched_links):
    """ Retrieves the latest news and parse its title/href """
    page = requests.get(NEWS_PATH)
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.findAll('li', {"id":re.compile("^post-")})
    for item in htmlTitles:
        txt_href = item.find('a')['href']
        txt_title = item.find('a').get('title')
        if txt_href and txt_href[:1] != '/':
            if is_not_fetched(fetched_links, txt_href):
                hrefs.append(txt_href)
                titles.append(txt_title)

def is_not_fetched(fetched_links, href):
    return href not in fetched_links

def get_news_content(news_path, paragraphs):
    """ Returns the paragraphs of the article """
    page = requests.get(news_path)
    soup = BeautifulSoup(page.text, 'html.parser')
    fullContent = soup.find(class_='article-content')

    # Get the texts that are outside paragraphs
    for without_paragraph_text in fullContent:
        text = str(without_paragraph_text).strip()
        # Ignore tags inside the text, in case it happens
        if should_add(text):
            paragraphs.append(sanitize_paragraph(text))
    fullContent = fullContent.find_all('p', recursive=False)

    # Get the texts that are inside paragraphs
    for i in range(0, len(fullContent) - 1):
        text = fullContent[i].getText()
        if should_add(text):
            paragraphs.append(sanitize_paragraph(text))


def sanitize_paragraph(paragraph):
    paragraph = paragraph.replace(u'\xa0', u' ')
    return paragraph


def should_add(text):
    return is_not_tag(text) and is_not_script_tag(text) and not is_useless_paragraph(text)


def is_not_script_tag(text):
    return text and "<script>" not in text


def is_useless_paragraph(paragraph):
    return paragraph.strip() == '' or paragraph.lower() == 'adiciona categoria materia'


def is_not_tag(text):
    return text and text[:1] != '<'


if __name__ == "__main__":
    scrap()
