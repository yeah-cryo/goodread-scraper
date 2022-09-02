"""
this module only contains Book class
"""
class Book:
    """
    A class to keep all the book attributes data.

    Attributes
    ----------
    book_url : str
        url of the book
    book_title : str
        the title of the book
    book_id : str
        the id of the book
    book_isbn : str
        the isnb of the book
    book_author_url : str
        the url of the author
    book_author : str
        the name of the author
    book_rating : str
        the rating of the book
    book_rating_counts : str
        the rating count of the book
    book_review_counts : str
        the review counts of the book
    book_img_url : str
        the image url of the book
    book_similar_url : str
        the simlar book url of the book
    """
    def __init__(self, book_url, book_title, book_id, book_isbn
                , book_author_url, book_author, book_rating, book_rating_counts
                , book_review_counts, book_img_url, book_similar_url):
        """
        initialize all the class attributes.
        """
        self.book_url = book_url
        self.book_title = book_title
        self.book_id = book_id
        self.book_isbn = book_isbn
        self.book_author_url = book_author_url
        self.book_author = book_author
        self.book_rating = book_rating
        self.book_rating_counts = book_rating_counts
        self.book_review_counts = book_review_counts
        self.book_img_url = book_img_url
        self.book_similar_url = book_similar_url

    def print_attribute(self):
        """
        print all the attributes.
        """
        print((self.book_url, self.book_title, self.book_id
        , self.book_isbn, self.book_author_url, self.book_author
        , self.book_rating,self.book_rating_counts, self.book_review_counts
        , self.book_img_url,self.book_similar_url))

    def write_book_to_db(self, cursor):
        """
        write the book attributes to the database.
        Parameters:
                cursor (cursor object of db): The cursor the the db. We can run sql code with this.
        """

        sql_code = """INSERT INTO books (book_url, title
        , book_id, ISBN, author_url, author, rating
        , rating_count, review_count, image_url ,similar_books) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            cursor.execute(sql_code, self.get_attributes())
        except Exception:
            print("err:unable to send data to the database")

    def get_attributes(self): # return attributes tuple for json parsing
        """"
        return attributes as a tuple
        """
        return (self.book_url, self.book_title
        , self.book_id, self.book_isbn
        , self.book_author_url, self.book_author
        , self.book_rating,self.book_rating_counts
        , self.book_review_counts, self.book_img_url
        ,self.book_similar_url)
