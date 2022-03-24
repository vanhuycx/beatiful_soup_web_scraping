import requests
from bs4 import BeautifulSoup

url="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

html_content = requests.get(url).text

soup = BeautifulSoup(html_content,'lxml')


# gdp_table = soup.find("table", attrs={"class": "wikitable sortabler"})
# gdp_table_headers = gdp_table.thead
# .find_all('tr')

gdp_table = soup.find("table", attrs={"class": "wikitable"})
gdp_table_data = gdp_table.tbody.find_all("tr") 

headings = []
for td in gdp_table_data[1].find_all("th"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.text)

print(headings)
# calculated_by = []
# for th in gdp_table_headers[0].find_all('th'):
#     calculated_by.append(th.text)

# print(calculated_by)

