"""
a collection of book scraping functions
"""
import requests
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer

def get_nxt_book_url(book_list_link, book_list):
    '''
    traversal through similar book page to find the next url for scraping.
        Parameters:
                similar_url (str): the url of similar book page.
                book_list (str): list of visited book url insures we won't visit a page twice.
        Returns:
                (str) the next book url to be scraped.
    '''
    page = requests.get(book_list_link)
    only_the_main_float = SoupStrainer('a', {"class" : 'gr-h3 gr-h3--serif gr-h3--noMargin'})
    soup = bs(page.content, 'html.parser', parse_only=only_the_main_float)
    titles = soup.find_all('a', {"class" : 'gr-h3 gr-h3--serif gr-h3--noMargin'}
    , {"itemprop": "url"})
    for title in titles:
        if not(("https://www.goodreads.com" + title['href']) in book_list):
            return "https://www.goodreads.com" + title['href']

def get_book_title(soup, cur_book_url):
    '''
    scrape the book title from certain author url.
        Parameters:
                soup (bs object): we can scrape book_title from this object.
        Returns:
            book_title (str) the scraped book title
    '''
    book_title = ''
    try:
        book_title = ((soup.find("h1"
        , {"id": "bookTitle"},{"itemprop": "name"}).get_text()).rstrip())[7:]
    except Exception:
        book_title = cur_book_url[len('https://www.goodreads.com/book/show/'):]
    return book_title

def get_book_id(book_url):
    '''
    scrape the book id from certain author url.
        Parameters:
                soup (bs object): we can scrape book_id from this object.
        Returns:
                book_id (str) the scraped book id
    '''
    temp = book_url.strip('https://www.goodreads.com/book/show/qwertyuioplkjhgfdsazxcvbnm-')
    book_id = ''
    for i in temp:
        if i.isdigit():
            book_id = book_id + i
    return book_id

def get_book_isbn(soup):
    '''
    scrape the book isbn from certain author url.
        Parameters:
                soup (bs object): we can scrape book_isbn from this object.
        Returns:
                book_isbn (str) the scraped book isbn.
    '''
    book_isbn = ''
    try:
        book_isbn = (soup.find("a", {"rel": "nofollow noopener"}))['href']
    except Exception:
        book_isbn = 'null'
    return book_isbn

def get_book_author_url(soup):
    '''
    scrape the book author's url from certain author url.
        Parameters:
                soup (bs object): we can scrape book_author_url from this object.
        Returns:
                book_author_url (str) the scraped book author url.
    '''
    book_author_url = ''
    try:
        book_author_url = soup.find("a", {"class": "authorName"}, {"itemprop": "url"})['href']
    except Exception:
        book_author_url = 'null'
    return book_author_url

def get_book_author(soup):
    '''
    scrape the book author's name from certain author url.
        Parameters:
                soup (bs object): we can scrape book_author from this object.
        Returns:
                book_author (str) the scraped book author.
    '''
    book_author = ''
    try:
        book_author = book_author = (soup.find("a", {"class": "authorName"}).get_text())
    except Exception:
        book_author = 'null'
    return book_author

def get_book_rating(soup):
    '''
    scrape the book's rating from certain author url.
        Parameters:
                soup (bs object): we can scrape book_rating from this object.
        Returns:
                book_rating (str) the scraped book rating.
    '''
    book_rating = ''
    try:
        book_rating = (soup.find("span", {"itemprop": "ratingValue"})).get_text().rstrip()[3:]
    except Exception:
        book_rating = 'null'
    return book_rating

def get_book_rating_counts(soup):
    '''
    scrape the book's rating count  from certain author url.
        Parameters:
                soup (bs object): we can scrape book_rating_counts from this object.
        Returns:
                book_rating_counts (str) the scraped book rating counts.
    '''
    book_rating_counts = ''
    try:
        book_rating_counts = (soup.find("meta", {"itemprop": "ratingCount"}))['content']
    except Exception:
        book_rating_counts = 'null'
    return book_rating_counts

def get_book_review_count(soup):
    '''
    scrape the book's review count from certain author url.
        Parameters:
                soup (bs object): we can scrape book_review_counts from this object.
        Returns:
                book_review_counts (str) the scraped book review counts.
    '''
    book_review_counts = ''
    try:
        book_review_counts = (soup.find("meta", {"itemprop": "reviewCount"}))['content']
    except Exception:
        book_review_counts = 'null'
    return book_review_counts

def get_book_img(soup):
    '''
    scrape the book's cover image from certain author url.
        Parameters:
                soup (bs object): we can scrape book_img from this object.
        Returns:
                book_img (str) the scraped book image.
    '''
    book_img = ''
    try:
        book_img = (soup.find("img", {"id": "coverImage"}))['src']
    except Exception:
        book_img = 'null'
    return book_img

def get_book_similar(soup):
    '''
    scrape the similar book of current book  from certain author url.
        Parameters:
                soup (bs object): we can scrape book_similar from this object.
        Returns:
                book_similar (str) the scraped similar book url.
    '''
    book_similar = ''
    try:
        book_similar = soup.find('a', {'class':'actionLink right seeMoreLink'})['href']
    except Exception:
        book_similar = 'null'
    return book_similar
