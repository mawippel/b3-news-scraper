import requests
from bs4 import BeautifulSoup


def scrap():
    print('Info Money Scraper!')

    hrefs = []
    titles = []
    paragraphs = []
    basepath = 'https://www.infomoney.com.br/mercados/ultimas-noticias'
    page = requests.get(basepath)
    soup = BeautifulSoup(page.text, 'html.parser')

    htmlTitles = soup.find_all(class_='title-box title-box-medium')
    # print(htmlTitles)
    for item in htmlTitles:
        hrefs.append(item['href'])
        titles.append(item.getText())
        # print(item)
        # print(item.getText())

    newsPath = 'https://www.infomoney.com.br/minhas-financas/consumo/noticia/8737584/varejo-devera-faturar-r-56-bilhoes-com-dia-dos-pais-diz-cnc'
    page = requests.get(newsPath)
    soup = BeautifulSoup(page.text, 'lxml')
    fullContent = soup.find(class_='article__content')
    for without_paragraph_text in fullContent:
        strContent = str(without_paragraph_text)
        strContent = strContent.strip()
        if strContent and strContent[:1] != '<':
            paragraphs.append(strContent)

    fullContent = fullContent.find_all('p', recursive=False)
    for i in range(0, len(fullContent) - 1):
        paragraphs.append(fullContent[i].getText())
    
    print(paragraphs)



if __name__ == "__main__":
    scrap()
