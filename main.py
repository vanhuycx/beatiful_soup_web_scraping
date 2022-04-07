import requests
from bs4 import BeautifulSoup
import pyodbc

# In SQLServer run query 'SELECT @@SERVERNAME' to check the server's name
Server = 'DESKTOP-13K0I1P'

try:
    sqlServerCon = pyodbc.connect('Driver={SQL Server};'
                      f'Server={Server};'
                      'Database=Books;'
                      'Trusted_Connection=yes;')
    sqlserver_create_table_query = '''CREATE TABLE Books (
                                    id INT IDENTITY(1,1) PRIMARY KEY,
                                    title VARCHAR(500) NOT NULL,                   
                                    price REAL NULL,
                                    in_stock INT NULL,
                                    rating VARCHAR(10) NULL,    
                                    genre VARCHAR(40) NULL,
                                    upc VARCHAR(20) NULL,
                                    description TEXT NULL                                                                  
                                    );'''
    drop_table = 'drop table if exists Books'

    # Create cursor connection to db
    cursor = sqlServerCon.cursor()
    print("Successfully Connected to SqlServer")

    # Drop Books table if exists and create a new one
    cursor.execute(drop_table)
    cursor.execute(sqlserver_create_table_query)
    sqlServerCon.commit()
    print("SqlServer table created")

    base_url =  'https://books.toscrape.com/catalogue/'

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
            price = book_article.find_all('p')[0].get_text()[2:]
            in_stock = book_article.find_all('p')[1].get_text().split()[2][1:] 
            rating = book_article.find_all('p')[2]['class'][1].lower()
            book_genre =  book_soup.find('ul',{'class':'breadcrumb'}).find_all('a')[2].get_text()
            description = ' '.join(book_soup.find_all('p')[3].get_text().replace("'", "&#39;").split()[:25]) + '...' # Get 25 beginning words
            upc = book_article.find('table').find_all('tr')[0].find('td').get_text()

            # Insert data row into table
            sqlserver_insert_query = f'INSERT INTO Books (title,price,in_stock,rating,genre,upc,description)  VALUES  ({repr(book_title)},{price},{in_stock},\'{rating}\',\'{book_genre}\',\'{upc}\',\'{description}\')'
            count = cursor.execute(sqlserver_insert_query)
            sqlServerCon.commit()

            print("Record inserted successfully into Books table ", cursor.rowcount)
            print(book_title,price,in_stock,rating,book_genre,description,upc)
            print('----------------------------------------')

    cursor.close()

except pyodbc.Error as error:
    print("Error while connecting to SqlServer - ", error)
finally:
    if sqlServerCon:
        sqlServerCon.close()
        print("The SqlServer connection is closed")