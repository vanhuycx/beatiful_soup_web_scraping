import requests
from bs4 import BeautifulSoup
import sqlite3


try:
    sqliteConnection = sqlite3.connect('SQLite_Python_test.db')
    sqlite_create_table_query = '''CREATE TABLE Books (
                                    id INTEGER PRIMARY KEY,                       
                                    title BLOB NOT NULL,                   
                                    price REAL NULL,
                                    in_stock INTEGER NULL,
                                    rating INTEGER NULL,
                                    genre TEXT NULL
                                                                
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

    

    book_title = '''Adulthood Is a Myth: A "Sarah's Scribbles" Collection '''.replace("'", "&#39;")

    sqlite_insert_query = f'INSERT INTO Books (title)  VALUES  ({repr(book_title)})'
    
    print(sqlite_insert_query)

    # print(sqlite_insert_query)
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)


    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqliteDB - ", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")