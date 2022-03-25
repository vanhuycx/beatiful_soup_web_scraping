import requests
from bs4 import BeautifulSoup
import sqlite3

try:
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    sqlite_create_table_query = '''CREATE TABLE Books (
                                    id INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL);'''
    drop_table = 'drop table if exists Books'

    # Create cursor connection to db
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    # Drop Books table if exists and create a new one
    cursor.execute(drop_table)
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    for index in range(1,51):
        url = f'https://books.toscrape.com/catalogue/page-{index}.html'
        result = requests.get(url)
        doc = BeautifulSoup(result.text,'html.parser')
        li_list = doc.find('section').find_all('div')[1].find('ol').find_all('li')
        for li_tag in li_list:
            book_title = li_tag.find('h3').string
            sqlite_insert_query = f'INSERT INTO Books (title)  VALUES  ({repr(f"{book_title}")})'
            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
            print(book_title)
            print('----------------------------------------')

    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")


