import requests
from bs4 import BeautifulSoup
import sqlite3


try:
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    sqlite_create_table_query = '''CREATE TABLE SqliteDb_developers (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    email text NOT NULL UNIQUE,
                                    joining_date datetime,
                                    salary REAL NOT NULL);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

# for index in range(1,51):
#     url = f'https://books.toscrape.com/catalogue/page-{index}.html'
#     result = requests.get(url)
#     doc = BeautifulSoup(result.text,'html.parser')
#     olist = doc.find('section').find_all('div')[1].find('ol')
#     for li_tag in olist.find_all('li'):
#         book_title = li_tag.find('h3').string
#         print(book_title)
#         # print('----------------------------------------')
