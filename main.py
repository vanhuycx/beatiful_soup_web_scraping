import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

result = requests.get(url)

doc = BeautifulSoup(result.text,'html.parser')

print(doc.prettify())
