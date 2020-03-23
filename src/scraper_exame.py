import requests
from bs4 import BeautifulSoup
from model.news import News
from database import Database

NEWS_PATH = 'https://exame.abril.com.br/noticias-sobre/acoes/'


def scrap():
    print('Starting Exame Scraper...')

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
    soup = BeautifulSoup(page.text, 'lxml')

    htmlTitles = soup.find_all(class_='list-item')
    for item in htmlTitles:
        txt_href = item.find('a')['href']
        txt_title = item.find('a').get('title')
        if txt_href and txt_href[:1] != '/':
            hrefs.append(txt_href)
            titles.append(txt_title)


def get_news_content(news_path, paragraphs):
    """ Returns the paragraphs of the article """
    page = requests.get(news_path)
    soup = BeautifulSoup(page.text, 'lxml')
    fullContent = soup.find(class_='article-content')

    # Get the texts that are outside paragraphs
    for without_paragraph_text in fullContent:
        text = str(without_paragraph_text).strip()
        # Ignore tags inside the text, in case it happens
        if is_not_tag(text):
            paragraphs.append(sanitize_paragraph(text))
    fullContent = fullContent.find_all('p', recursive=False)

    # Get the texts that are inside paragraphs
    for i in range(0, len(fullContent) - 1):
        text = fullContent[i].getText()
        if is_not_script_tag(text):
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
