import requests
from bs4 import BeautifulSoup

NEWS_PATH = 'https://exame.abril.com.br/noticias-sobre/acoes/'


def scrap():
    print('Starting Exame Scraper...')

    hrefs = []
    titles = []
    paragraphs = []

    get_news(hrefs, titles)
    print(hrefs, titles)
    for href in hrefs:
        get_news_content(href, paragraphs)
        print(paragraphs)
    # news_path = 'https://exame.abril.com.br/mercados/a-bolsa-despencou-e-hora-de-comprar/'
    # get_news_content(news_path, paragraphs)


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
            paragraphs.append(text)
    fullContent = fullContent.find_all('p', recursive=False)

    # Get the texts that are inside paragraphs
    for i in range(0, len(fullContent) - 1):
        text = fullContent[i].getText()
        if is_not_script_tag(text):
            paragraphs.append(text)


def is_not_script_tag(text):
    return text and "<script>" not in text


def is_not_tag(text):
    return text and text[:1] != '<'


if __name__ == "__main__":
    scrap()
