"""scraper.py scrapes the both book and author, and put them to mysql db."""
import os
import sys
import argparse
from threading import Thread, Lock
import requests
import mysql.connector
from bs4 import SoupStrainer
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from book import Book
from author import Author
from scrape_book_call import *
from scrape_author_call import *
from json_parser import *
from api_functionality import *

#program setup

# arguments accept valid starting url,
# number of books ranging in 200-2001
# and number of authors ranging in 50-2001
parser = argparse.ArgumentParser()
parser.add_argument(dest='argument1', type=str, help="starting url")
parser.add_argument(dest='argument2', type=int,choices=range(200,2001), help="number of books")
parser.add_argument(dest='argument3', type=int,choices=range(50,2001), help="number of authors")
parser.add_argument('dir', nargs='*')
args = parser.parse_args()
URL = args.argument1
BOOK_COUNTS = args.argument2
AUTHOR_COUNTS = args.argument3
args_list = args.dir

# check if statring url valid
if URL[:len("https://www.goodreads.com/book/show/")] != "https://www.goodreads.com/book/show/":
    print(URL[:len("https://www.goodreads.com/book/show/")])
    sys.exit("incorrect starting url.")

#program setup

# connect to local db goodreadscrape
load_dotenv()
mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('USER'),
  password=os.getenv('PASSWORD'),
  database="goodreadscrape"
)
mycursor = mydb.cursor() # mysql db cursor

WRITE_FILE_TO_DB_AUTHOR = 'afb'
WRITE_FILE_TO_DB_BOOK = 'bfb'
WRITE_DB_TO_FILE_AUTHOR = 'abf'
WRITE_DB_TO_FILE_BOOK = 'bbf'
THREAD_COUNT = 4
BOOK_COUNTS -= THREAD_COUNT
AUTHOR_COUNTS -= THREAD_COUNT
BOOK_SIMILAR_URLS = 'null'
CUR_AUTHOR_URLS = 'null'
AUTHOR_SIMILAR_URLS = 'null'

# checking arguments
if len(args_list) != 0 and args_list[0] != 'draw':
    print(args_list)
    if args_list[0] == 'GET':
        output = get_processor(mycursor, args_list[1], args_list[2])
        if output == 'null':
            sys.exit("program failed, please check your parameters")
        sys.exit(output)
    elif args_list[0] == 'PUT':
        if put_processor(mydb, mycursor, args_list[1], args_list[2], args_list[3], args_list[4]) == 'null':
            sys.exit("program failed, please check your parameters")
        sys.exit('PUT success')
    elif args_list[0] == 'POST':
        if args_list[1] == 'scrape':
            if post_query(mydb, mycursor, 'scrape',args_list[2], '') == 'null':
                sys.exit("program failed, please check your parameters")
        else:
            if post_query(mydb, mycursor, args_list[1],'', args_list[2]) == 'null':
                sys.exit("program failed, please check your parameters")
        sys.exit('POST success')
    elif args_list[0] == 'delete':
        if delete_processor(mydb, mycursor, args_list[1], args_list[2]) == 'null':
            sys.exit("program failed, please check your parameters")
        sys.exit('DELETE success')
    else:
        if args_list[0].split('.')[1] != 'json':
            sys.exit('not a json file')
        if len(args_list) < 2:
            sys.exit("incorrect arguments number")
        if args_list[1] == WRITE_FILE_TO_DB_AUTHOR:
            write_json_to_db_author(mycursor, args_list[0])
            mydb.commit()
        elif args_list[1] == WRITE_FILE_TO_DB_BOOK:
            write_json_to_db_book(mycursor, args_list[0])
            mydb.commit()
        elif args_list[1] == WRITE_DB_TO_FILE_AUTHOR:
            write_db_author_to_file(mycursor, args_list[0])
            mydb.commit()
        elif args_list[1] == WRITE_DB_TO_FILE_BOOK:
            write_db_book_to_file(mycursor, args_list[0])
            mydb.commit()
        else:
            sys.exit("incorrect 5th arguments")
    sys.exit("program exit")

book_mutex = Lock() # mutex lock for book loop
author_mutex = Lock() # mutex lock for author loop
db_mutex = Lock() # mutex lock makes sure only one thread can access dn at a time

def scrape_author_loop(start_author_url, cursor, my_db):
    '''
    traversal through author page urls to scrape data, then send the collected author data to db.
        Parameters:
                start_author_url (str): the starting url of this traversal.
                cursor, my_db (mysql object): mysql object that is used to write data into db.
    '''
    global AUTHOR_COUNTS
    author_url = start_author_url
    author_mutex.acquire()
    while AUTHOR_COUNTS > 0:
        print("author_remaining :" + str(AUTHOR_COUNTS), len(author_list))
        author_mutex.release()
        # scrape content of current url
        page = requests.get(author_url)
        soup = bs(page.text, 'html.parser')
        author_similar_url = get_similar_author(soup)
        if author_similar_url == 'null':
            author_mutex.acquire()
            continue
        cur_author = Author(get_author_name(soup)
        , author_url, get_author_id(author_url)
        , get_author_rating(soup)
        , get_author_rating_count(soup)
        , get_author_review_count(soup)
        , get_author_img(soup)
        , author_similar_url, get_list_books(soup))
        cur_author.print_attribute()
        # find the next url
        page = requests.get(author_similar_url)
        only_a_1 = SoupStrainer('a')
        soup = bs(page.content, 'html.parser', parse_only=only_a_1)
        titles = soup.find_all('a', {"class" : 'gr-h3 gr-h3--serif gr-h3--noMargin'}
                                , {"itemprop": "url"})
        author_mutex.acquire()
        url_save = author_url
        for title in titles:
            if not (title['href'] in author_list):
                author_url =  title['href']
                break
        if (author_url == 'null' or author_url is None):
            author_url = url_save
            continue
        # write the data to database
        db_mutex.acquire()
        cur_author.write_author_to_db(cursor)
        my_db.commit()
        db_mutex.release()
        # add author url to the traversed url_list
        author_list.append(author_url)
        AUTHOR_COUNTS -= 1
    author_mutex.release()

def scrape_book_loop(book_url, cursor, my_db, graph):
    '''
    traversal through book page urls to scrape data, then send the collected author data to db.
        Parameters:
                book_url (str): the starting url of this traversal.
                cursor, my_db (mysql object): mysql object that is used to write data into db.
    '''
    global BOOK_COUNTS
    cur_book_url = book_url
    book_mutex.acquire()
    while BOOK_COUNTS > 0: # book page scraping loop
        print("book_remaining :" + str(BOOK_COUNTS), len(book_list))
        book_mutex.release()
        # get the similar book url
        only_a = SoupStrainer('a', {'class':'actionLink right seeMoreLink'})
        page = requests.get(cur_book_url)
        soup = bs(page.text, 'html.parser', parse_only=only_a)
        book_similar_url = get_book_similar(soup)
        if book_similar_url == 'null':
            book_mutex.acquire()
            continue
        # get all other attributes, and assemble them into the Book object
        only_topcol = SoupStrainer(id="topcol")
        soup = bs(page.text, 'html.parser', parse_only=only_topcol)
        book_author = get_book_author(soup)
        book_title = get_book_title(soup, cur_book_url)
        cur_book = Book(cur_book_url, book_title
        ,get_book_id(cur_book_url), get_book_isbn(soup)
        , get_book_author_url(soup), book_author
        ,  get_book_rating(soup), get_book_rating_counts(soup)
        , get_book_review_count(soup),get_book_img(soup), book_similar_url)
        cur_book.print_attribute()
        # find the next book url of this traversal
        page = requests.get(book_similar_url)
        only_a_gr = SoupStrainer('a', {"class" : 'gr-h3 gr-h3--serif gr-h3--noMargin'})
        soup = bs(page.content, 'html.parser', parse_only=only_a_gr)
        titles = soup.find_all('a', {"class" : 'gr-h3 gr-h3--serif gr-h3--noMargin'}
                                , {"itemprop": "url"})
        book_mutex.acquire()
        url_save = cur_book_url
        for title in titles:
            if not(("https://www.goodreads.com" + title['href']) in book_list):
                cur_book_url =  "https://www.goodreads.com" + title['href']
                break
        if (cur_book_url == 'null' or cur_book_url is None):
            cur_book_url = url_save
            continue
        db_mutex.acquire()
        if book_author!= 'null':
            graph.add_edge(book_title, book_author)
        cur_book.write_book_to_db(cursor)
        my_db.commit()
        db_mutex.release()
        book_list.append(cur_book_url)
        BOOK_COUNTS -= 1
    book_mutex.release()

# the scrape program #



book_list = [URL] # list of scraped authot url

# get the Similar book url and starting author url for preparing the traversal
while BOOK_SIMILAR_URLS == 'null' or CUR_AUTHOR_URLS == 'null':
    page_b = requests.get(URL)
    only_the_main_float = SoupStrainer('a')
    soup_b = bs(page_b.text, 'html.parser', parse_only=only_the_main_float)
    BOOK_SIMILAR_URLS = get_book_similar(soup_b)
    CUR_AUTHOR_URLS = get_book_author_url(soup_b)

author_list = [CUR_AUTHOR_URLS] # list of scraped book url
while AUTHOR_SIMILAR_URLS == 'null':
    page_a = requests.get(CUR_AUTHOR_URLS)
    only_the_main_float = SoupStrainer('a')
    soup_a = bs(page_a.text, 'html.parser', parse_only=only_the_main_float)
    AUTHOR_SIMILAR_URLS = get_similar_author(soup_a)

# add the starting urls into list of "visited" for both author and book
for index in range(THREAD_COUNT - 1):
    t_next_book_url = get_nxt_book_url(BOOK_SIMILAR_URLS, book_list)
    while t_next_book_url == "null":
        print(len(book_list))
        t_next_book_url = get_nxt_book_url(BOOK_SIMILAR_URLS, book_list)
    t_next_author_url = get_next_author_url(AUTHOR_SIMILAR_URLS, author_list)
    while t_next_author_url == 'null':
        print(len(author_list))
        t_next_author_url = get_next_author_url(AUTHOR_SIMILAR_URLS, author_list)
    book_list.append(get_nxt_book_url(BOOK_SIMILAR_URLS, book_list))
    author_list.append(get_next_author_url(AUTHOR_SIMILAR_URLS, author_list))

book_threads = []
author_threads = []
# create THREAD_COUNT number of thread
# for both book scraper and author scraper
G = nx.Graph()
for index in range(THREAD_COUNT):
    book_t = Thread(target = scrape_book_loop, args = (book_list[index], mycursor, mydb, G))
    author_t = Thread(target = scrape_author_loop, args = (author_list[index], mycursor, mydb))
    book_threads.append(book_t)
    author_threads.append(author_t)
# start all the threads
for index in range(THREAD_COUNT):
    book_threads[index].start()
    author_threads[index].start()
# Wait for all of threads to finish
for index in range(THREAD_COUNT):
    book_threads[index].join()
    author_threads[index].join()

if args_list[0] == 'draw':
    subax1 = plt.subplot(122)
    nx.draw(G, with_labels=True)
    plt.show()