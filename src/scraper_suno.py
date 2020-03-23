import requests
from bs4 import BeautifulSoup
from model.news import News
from database import Database

NEWS_PATH = 'https://www.sunoresearch.com.br/noticias/mercado/'


def scrap():
    print('Starting Suno Scraper...')
    db = Database()

    news = []
    paragraphs = []
    hrefs, titles = get_news()
    print(hrefs, titles)
    for i in range(0, len(hrefs)):
        get_news_content(hrefs[i], paragraphs)
        news.append(News(titles[i], hrefs[i], paragraphs))
        paragraphs = []

    for el in news:
        db.save(el)
    print('All news were saved.')


def get_news():
    hrefs = []
    titles = []

    page = requests.get(NEWS_PATH)
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.find_all(class_='list-item')
    for item in htmlTitles:
        title = item.find('h3', {'class': 'post__title'})
        txt_href = title.find('a')['href']
        txt_title = title.find('a').text
        hrefs.append(txt_href)
        titles.append(txt_title)
    return hrefs, titles


def get_news_content(news_path, paragraphs):
    """ Returns the paragraphs of the article """
    page = requests.get(news_path)
    soup = BeautifulSoup(page.text, 'lxml')
    fullContent = soup.find('div', itemprop="articleBody")
    # Get the texts that are outside paragraphs
    article_paragraphs = fullContent.find_all('p')
    for paragraph in article_paragraphs:
        text = paragraph.getText()
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
