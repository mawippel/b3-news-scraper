import requests
from bs4 import BeautifulSoup

NEWS_PATH = 'https://www.sunoresearch.com.br/noticias/mercado/'

def scrap():
  print('Starting Suno Scraper...')
  hrefs, titles = get_news()
  print(hrefs, titles)

def get_news():
  hrefs = []
  titles = []

  page = requests.get(NEWS_PATH)
  soup = BeautifulSoup(page.text, 'html.parser')
  
  htmlTitles = soup.find_all(class_='list-item')
  for item in htmlTitles:
    title = item.find('h3', {'class':'post__title'})
    txt_href = title.find('a')['href']
    txt_title = title.find('a').text
    hrefs.append(txt_href)
    titles.append(txt_title)
  return hrefs, titles

if __name__ == "__main__":
    scrap()