"""
a collection of function that responsible for
communication between database and the scraping program.
"""
import json
from author import Author
from book import Book
from dic_tuple_converter import *
def write_db_book_to_file(cursor, filename):
    '''
    write content in book database into certain file.
        Parameters:
                cursor (cursor object of db): The cursor the the db. We can run sql code with this.
                filename (str): the filename of the json write-file.
    '''
    cursor.execute("SELECT * FROM books")
    query_result = cursor.fetchall()
    with open(filename,'w+') as file:
        file_data = {'books':[]}
        for cur_tuple in query_result:
            file_data['books'].append(tuple_to_json_converter_book(cur_tuple))
        json.dump(file_data, file, indent = 4)

def write_db_author_to_file(cursor, filename):
    '''
    write content in author database into certain file.
        Parameters:
                cursor (cursor object of db): The cursor the the db. We can run sql code with this.
                filename (str): the filename of the json write-file.
    '''
    cursor.execute("SELECT * FROM authors")
    query_result = cursor.fetchall()
    with open(filename,'w+') as file:
        file_data = {'authors':[]}
        for cur_tuple in query_result:
            file_data['authors'].append(tuple_to_json_converter_author(cur_tuple))
        json.dump(file_data, file, indent = 4)

def write_json_to_db_book(cursor, filename):
    '''
    read certain json file and write the content into database.
        Parameters:
                cursor (cursor object of db): The cursor the the db. We can run sql code with this.
                filename (str): the filename of the json write-file.
    '''
    try:
        with open(filename,'r+') as file:
            data = json.load(file)
            for dic in data['books']:
                cur_tuple = json_to_tuple_converter_book(dic)
                (url, title, b_id, isbn, a_url
                , author, rating, rating_c
                , review_c, image, similar_book) = cur_tuple
                book = Book(url, title, b_id
                            , isbn, a_url, author, rating
                            , rating_c, review_c, image, similar_book)
                book.write_book_to_db(cursor)
    except Exception:
        print('fail to convert, please check your input file.')

def write_json_to_db_author(cursor, filename):
    '''
    read certain json file and write the content into database.
        Parameters:
                cursor (cursor object of db): The cursor the the db. We can run sql code with this.
                filename (str): the filename of the json write-file.
    '''
    try:
        with open(filename,'r+') as file:
            data = json.load(file)
            for dic in data['authors']:
                cur_tuple = json_to_tuple_converter_author(dic)
                (name, url, a_id, rating
                , rating_count, review_count
                , image, authors, books) =cur_tuple
                author =Author(name, url, a_id, rating
                                , rating_count, review_count
                                , image, authors, books)
                author.write_author_to_db(cursor)
    except Exception:
        print('fail to convert, please check your input file.')
