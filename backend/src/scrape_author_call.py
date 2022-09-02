"""
a collection of author scraping functions
"""
import requests
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer


def get_next_author_url(similar_url, author_list):
    '''
    traversal through similar author page to find the next url for scraping.
        Parameters:
                similar_url (str): the url of similar author page.
                author_list (str): list of visited author url insures we won't visit a page twice.
        Returns:
                (str) the next author url to be scraped.
    '''
    page = requests.get(similar_url)
    only_the_main_float = SoupStrainer('a')
    soup = bs(page.content, 'html.parser', parse_only=only_the_main_float)
    titles = soup.find_all('a', {"class" : 'gr-h3 gr-h3--serif gr-h3--noMargin'}
    , {"itemprop": "url"})
    for title in titles:
        if not(title['href']) in author_list:
            return title['href']
    return 'null'

def get_author_name(soup):
    '''
    scrape the author name from certain author url.
        Parameters:
                soup (bs object): we can scrape author_name from this object.
        Returns:
                author_name (str) the author name.
    '''
    author_name = ''
    try:
        author_name = (soup.find("h1", {'class': 'authorName'}).get_text()).rstrip()[1:]
    except Exception:
        author_name = 'null'
    return author_name

def get_author_id(book_author_url):
    '''
    scrape the author id from certain author url.
        Parameters:
                soup (bs object): we can scrape author_id from this object.
        Returns:
                author_id (str) the author id.
    '''
    temp_author = book_author_url.strip("https://www.goodreads.com/author/show/")[:7]
    author_id = ''
    for i in temp_author:
        if i.isdigit():
            author_id = author_id + i
    return author_id

def get_author_rating(soup):
    '''
    scrape the author's rating from certain author url.
        Parameters:
                soup (bs object): we can scrape author_rating from this object.
        Returns:
                author_rating (str) the author's rating.
    '''
    author_rating = ''
    try:
        author_rating = (soup.find("span", {"itemprop": "ratingValue"})).get_text().rstrip()
    except Exception:
        author_rating = 'null'
    return author_rating

def get_author_rating_count(soup):
    '''
    scrape the author's rating count from certain author url.
        Parameters:
                soup (bs object): we can scrape author_rating_count from this pbject.
        Returns:
                author_rating_count (str) the author's rating count.
    '''
    author_rating_count = ''
    try:
        author_rating_count = (soup.find("span", {"itemprop": "ratingCount"}))['content']
    except Exception:
        author_rating_count = 'null'
    return author_rating_count

def get_author_review_count(soup):
    '''
    scrape the author's review count from certain author url.
        Parameters:
                soup (bs object): we can scrape author_review_count from this object.
        Returns:
                author_review_count (str) the author's review count.
    '''
    author_review_count = ''
    try:
        author_review_count = (soup.find("span", {"itemprop": "reviewCount"}))['content']
    except Exception:
        author_review_count = 'null'
    return author_review_count

def get_author_img(soup):
    '''
    scrape the author's image from certain author url.
        Parameters:
                soup (bs object): we can scrape author_img from this object.
        Returns:
                author_img (str) the author's image.
    '''
    author_img = ''
    try:
        author_img = (soup.find("img", {"itemprop": "image"}))['src']
    except Exception:
        author_img = 'null'
    return author_img

def get_similar_author(soup):
    '''
    scrape the author's similar authors from certain author url.
        Parameters:
                soup (bs object): we can scrape similar_author from this object.
        Returns:
                author_similar (str) the similar author url.
    '''
    author_similar = ''
    try:
        author_similar = "https://www.goodreads.com" + soup.find('a'
        , text = "Similar authors")['href']
    except Exception:
        author_similar = 'null'
    return author_similar

def get_list_books(soup):
    '''
    scrape the author's books from certain author url.
        Parameters:
                soup (bs object): we can scrape get_list_books from this object.
        Returns:
                blist (str) the author's books.
    '''
    book_list = []
    try:
        book_list = soup.find_all('a', class_ = "bookTitle")
    except Exception:
        book_list = []
    blist = ''
    for index,ele in enumerate(book_list):
        blist = blist + ele.get_text().rstrip()[1:] + ';'
        if index >= 1:
            break
    return blist
