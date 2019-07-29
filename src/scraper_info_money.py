import requests
from bs4 import BeautifulSoup


def crawl():
    basepath = 'https://www.infomoney.com.br/mercados/ultimas-noticias'
    page = requests.get(basepath)
    soup = BeautifulSoup(page.text, 'html.parser')

    artist_name_list = soup.find_all(class_='title-box title-box-medium')
    print(artist_name_list)
    for item in artist_name_list:
        print(item)


if __name__ == "__main__":
    crawl()
