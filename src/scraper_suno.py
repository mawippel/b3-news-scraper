import requests
from bs4 import BeautifulSoup

NEWS_PATH = 'https://www.sunoresearch.com.br/noticias/mercado/'


def scrap():
    print('Starting Suno Scraper...')
    hrefs, titles = get_news()
    print(hrefs, titles)
    # for href in hrefs:
    #     get_news_content(href, paragraphs)
    paragraphs = get_news_content('https://www.sunoresearch.com.br/noticias/ibovespa-queda-05022020/')
    print(paragraphs)


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


def get_news_content(news_path):
    """ Returns the paragraphs of the article """
    paragraphs = []
    page = requests.get(news_path)
    soup = BeautifulSoup(page.text, 'lxml')
    fullContent = soup.find('div', itemprop="articleBody")
    # Get the texts that are outside paragraphs
    article_paragraphs = fullContent.find_all('p')
    for paragraph in article_paragraphs:
        text = paragraph.getText()
        paragraphs.append(text)
    return paragraphs


if __name__ == "__main__":
    scrap()
