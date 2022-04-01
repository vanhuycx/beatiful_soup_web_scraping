import urllib
import requests
from bs4 import BeautifulSoup
import sqlite3

try:

    sqliteConnection = sqlite3.connect('SQLite_Python_test.db')
    sqlite_create_table_query = '''CREATE TABLE Books (
                                    id INTEGER PRIMARY KEY,                       
                                    title TEXT NOT NULL,                   
                                    price REAL NULL,
                                    in_stock INTEGER NULL,
                                    rating INTEGER NULL,
                                    genre TEXT NULL,
                                    description TEXT NULL,                      
                                    UPC TEXT NULL                      
                                    );'''
    drop_table = 'drop table if exists Books'

    # Create cursor connection to db
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    # Drop Books table if exists and create a new one
    cursor.execute(drop_table)
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")
   

    base_url =  'https://books.toscrape.com/catalogue/'

    google_search_url = 'https://www.google.com/search?tbm=bks&q='

    for index in range(1,51):
        url = f'https://books.toscrape.com/catalogue/page-{index}.html'
        page_request = requests.get(url)
        page_soup = BeautifulSoup(page_request.text,'html.parser')
        li_list = page_soup.find('section').find_all('div')[1].find('ol').find_all('li')
        #Loop through li_list 
        for li_tag in li_list:
            # For each li tag, find the href, create, and access the book full link to create the book soup object
            full_book_link = base_url + li_tag.find('h3').find('a')['href']
            book_request =  requests.get(full_book_link)
            book_soup = BeautifulSoup(book_request.text,'html.parser')
            
            # Create the book article object
            book_article = book_soup.find('article')
            # Then, find information about book by finding the element and accessing the attribute(s)
            book_title = book_article.find('h1').get_text().replace("'", "&#39;") # Replace single quote with the UTF-8 representation

            google_search_request = requests.get(google_search_url + urllib.parse.quote_plus(str(book_title)))
            # print(google_search_url+urllib.parse.quote_plus(str(book_title)))
            google_book_soup = BeautifulSoup(google_search_request.text,'html.parser')

            book_author = google_book_soup.find_all('div',class_='BNeawe s3v9rd AP7Wnd')
            print(book_author)


            # price = book_article.find_all('p')[0].get_text()[2:]
            # in_stock = book_article.find_all('p')[1].get_text().split()[2][1:] 
            # rating = book_article.find_all('p')[2]['class'][1].lower()
            # book_genre =  book_soup.find('ul',{'class':'breadcrumb'}).find_all('a')[2].get_text()
            # description = ' '.join(book_soup.find_all('p')[3].get_text().replace("'", "&#39;").split()[:25]) + '...' # Split and join 25 beginning words
            # upc = book_article.find('table').find_all('tr')[0].find('td').get_text()
            
            
            # product_type = book_article.find('table').find_all('tr')[1].find('td').get_text()
            # tax = book_article.find('table').find_all('tr')[4].find('td').get_text()[2:]
            # review_num = book_article.find('table').find_all('tr')[6].find('td').get_text()


            
            # sqlite_insert_query = f'INSERT INTO Books (title,price,in_stock,rating,genre,description)  VALUES  ({repr(book_title)},{price},{in_stock},\'{rating}\',\'{book_genre}\',\'{description}\')'

            # count = cursor.execute(sqlite_insert_query)
            # sqliteConnection.commit()

            # print("Record inserted successfully into Books table ", cursor.rowcount)
            # print(book_title,price,in_stock,rating,book_genre,description,upc)
            # print('----------------------------------------')

    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqliteDB - ", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")