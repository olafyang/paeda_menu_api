import requests
from bs4 import BeautifulSoup


def scrap_pdf():
    url_to_scrap = 'https://www.internats-gymnasium.de/service/plaene.html'
    html = requests.get(url_to_scrap).text
    soup = BeautifulSoup(html, 'html.parser')
    url = soup.strong.parent.parent.get('href')

    file = requests.get(url, allow_redirects=True).content
    return file
