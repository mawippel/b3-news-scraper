import requests
from bs4 import BeautifulSoup

BASE_PATH = 'https://www.infomoney.com.br'
NEWS_PATH = BASE_PATH + '/mercados/ultimas-noticias'


def scrap():
    print('Starting Info Money Scraper...')

    hrefs = []
    titles = []
    paragraphs = []

    get_news(hrefs, titles)
    # for title in titles:
    #     news_path = BASE_PATH + title
    #     get_news_content(news_path, paragraphs)
    news_path = BASE_PATH + '/mercados/politica/noticia/8787554/empresario-flavio-rocha-fala-sobre-imposto-unico-na-reforma-tributaria-acompanhe'
    get_news_content(news_path, paragraphs)
    print(paragraphs)


def get_news(hrefs, titles):
    """ Retrieves the latest news and parse its title/href """
    page = requests.get(NEWS_PATH)
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.find_all(class_='title-box title-box-medium')
    for item in htmlTitles:
        hrefs.append(item['href'])
        titles.append(item.getText())


def get_news_content(news_path, paragraphs):
    page = requests.get(news_path)
    soup = BeautifulSoup(page.text, 'lxml')
    fullContent = soup.find(class_='article__content')

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
