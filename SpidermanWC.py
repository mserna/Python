import requests
from bs4 import BeautifulSoup

def find_tickets_spider(max_pages):
    page = 1
    while page != 0:
        url = 'https://www.ticketmaster.com/'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', {'class': 'event'}):
            href = link.get('href')
            title = link.string
            print(href)
            print(title)

find_tickets_spider(1)