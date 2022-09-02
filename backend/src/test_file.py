import unittest
import requests
from book import Book
from author import Author
from bs4 import BeautifulSoup as bs
from json_parser import *
from scrape_author_call import *
from scrape_book_call import *
class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        page_book = requests.get('https://www.goodreads.com/book/show/19288043-gone-girl')
        self.soup_book = bs(page_book.content, 'html.parser')
        page_author = requests.get('https://www.goodreads.com/author/show/2383.Gillian_Flynn')
        self.soup_author = bs(page_author.content, 'html.parser')
    
    def test_tuple_to_json_converter_book(self):
        test_tp = ('book_url', 'title'
        , 'book_id', 'ISBN', 'author_url', 'author', 'rating'
        , 'rating_count', 'review_count', 'image_url' ,'similar_books')
        test_dic = tuple_to_json_converter_book(test_tp)
        for ele in test_tp:
            self.assertEqual(ele, test_dic[ele]
            , "data mismatch after convertion : tuple_to_json_converter_book")
        
    def test_tuple_to_json_converter_author(self):
        test_tp = ('name', 'author_url'
        , 'author_id', 'rating'
        , 'rating_count', 'review_count'
        , 'image_url', 'related_authors', 'author_books')
        test_dic = tuple_to_json_converter_author(test_tp)
        for ele in test_tp:
            self.assertEqual(ele, test_dic[ele])

    def test_json_to_tuple_converter_author(self):
        test_dic = {'name':'name','author_url':'author_url'
        , 'author_id':'author_id', 'rating':'rating'
        , 'rating_count':'rating_count', 'review_count':'review_count'
        , 'image_url':'image_url', 'related_authors':'related_authors'
        ,'author_books':'author_books'}
        test_tp = json_to_tuple_converter_author(test_dic)
        for ele in test_tp:
            self.assertEqual(ele, test_dic[ele]
            , "data mismatch after convertion : json_to_tuple_converter_author")

    def test_json_to_tuple_converter_book(self):
        test_dic = {'book_url':'book_url','title':'title'
        , 'book_id':'book_id', 'ISBN':'ISBN'
        , 'author_url':'author_url', 'author':'author'
        , 'rating':'rating', 'rating_count':'rating_count'
        ,'review_count':'review_count', 'image_url':'image_url'
        ,'similar_books':'similar_books'}
        test_tp = json_to_tuple_converter_book(test_dic)
        for ele in test_tp:
            self.assertEqual(ele, test_dic[ele]
            , "data mismatch after convertion : json_to_tuple_converter_book")
    
    def test_author_get_attribute(self):
        test_tp = ('name', 'author_url'
        , 'author_id', 'rating'
        , 'rating_count', 'review_count'
        , 'image_url', 'related_authors', 'author_books')

        (name, url, a_id, rating
                , rating_count, review_count
                , image, authors, books) =test_tp
        test_author = Author(name, url, a_id, rating
                , rating_count, review_count
                , image, authors, books)
        self.assertEqual(test_tp, test_author.get_attributes()
        , "get_attribute() gets wrong attributes")

    def test_book_get_attribute(self):
        test_tp = ('book_url', 'title'
        , 'book_id', 'ISBN', 'author_url', 'author', 'rating'
        , 'rating_count', 'review_count', 'image_url' ,'similar_books')
        (url, title, b_id, isbn, a_url
                , author, rating, rating_c
                , review_c, image, similar_book) = test_tp
        test_book = Book(url, title, b_id
                , isbn, a_url, author, rating
                , rating_c, review_c, image, similar_book)
        self.assertEqual(test_tp, test_book.get_attributes()
        , "get_attribute() gets wrong attributes")

    def test_get_book_title(self):
        test_title = get_book_title(self.soup_book
        , 'https://www.goodreads.com/book/show/19288043-gone-girl')
        true_list = ["Gone Girl", 'null', '19288043-gone-girl']
        self.assertIn(test_title, true_list, "get_book_title() gives the wrong data")

    def test_get_book_id(self):
        test_id = get_book_id('https://www.goodreads.com/book/show/19288043-gone-girl')
        self.assertEqual('19288043', test_id, "get_book_id() gives wrong id")

    def test_get_book_isbn(self):
        test_isbn = get_book_isbn(self.soup_book)
        true_list = ['null', 'https://www.goodreads.com/book/show/12749.Swann_s_Way__In_Search_of_Lost_Time___1_']
        self.assertIn(test_isbn, true_list, "get_book_isbn() gives the wrong data")

    def test_get_book_author_url(self):
        test_author_url = get_book_author_url(self.soup_book)
        true_list = ['null', 'https://www.goodreads.com/author/show/2383.Gillian_Flynn']
        self.assertIn(test_author_url, true_list, "get_book_author_url() gives the wrong data")

    def test_get_book_author(self):
        test_book_author = get_book_author(self.soup_book)
        true_list = ['null', 'Gillian Flynn']
        self.assertIn(test_book_author, true_list, "get_book_author() gives the wrong data")

    def test_get_book_rating(self):
        test_book_rating = get_book_rating(self.soup_book)
        true_list = ['null', '4.09']
        self.assertIn(test_book_rating, true_list, "get_book_rating() gives the wrong data")

    def test_get_book_img(self):
        test_book_img = get_book_img(self.soup_book)
        true_list = ['null', 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1554086139l/19288043.jpg']
        self.assertIn(test_book_img, true_list, "get_book_img() gives the wrong data")

    def test_get_book_similar(self):
        test_book_similar = get_book_similar(self.soup_book)
        true_list = ['null', 'https://www.goodreads.com/book/similar/13306276-gone-girl']
        self.assertIn(test_book_similar, true_list, "get_book_similar() gives the wrong data")
    
    def test_get_author_name(self):
        test_author_name = get_author_name(self.soup_author)
        true_list = ['null', 'Gillian Flynn']
        self.assertIn(test_author_name, true_list, "get_author_name() gives the wrong data")

    def test_get_author_id(self):
        test_author_id = get_author_id('https://www.goodreads.com/author/show/2383.Gillian_Flynn')
        true_list = ['null', '2383']
        self.assertIn(test_author_id, true_list, "get_author_id() gives the wrong data")

    def test_get_author_rating(self):
        test_author_rating = get_author_rating(self.soup_author)
        true_list = ['null', '4.03']
        self.assertIn(test_author_rating, true_list, "get_author_rating() gives the wrong data")

    def test_get_author_img(self):
        test_author_img = get_author_img(self.soup_author)
        true_list = ['null', 'https://images.gr-assets.com/authors/1232123231p5/2383.jpg']
        self.assertIn(test_author_img, true_list, "get_author_img() gives the wrong data")

# name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books
#'Gillian Flynn', 'https://www.goodreads.com/author/show/2383.Gillian_Flynn'
# , '2383', '4.03', '4320673', '254746'
# , 'https://images.gr-assets.com/authors/1232123231p5/2383.jpg'
# , 'https://www.goodreads.com/author/similar/2383.Gillian_Flynn'
# , 'Gone Girl;Dark Places;'


if __name__ == '__main__':
    
    unittest.main()