"""
this module only contains Author class
"""
class Author:
    """
    A class to keep all the author attributes data.

    Attributes
    ----------
    name : str
        name of the author
    author_url : str
        the url of the author page
    author_id : str
        the id of the author
    rating : str
        the rating of the author
    rating_count : str
        the rating count of the author
    review_count : str
        the review count of the author
    image_url : str
        the image url of the author
    related_authors : str
        the realated authors of the author
    author_books : str
        the books of the author
    """
    def __init__(self, name, author_url, author_id, rating
                , rating_count, review_count, image_url, related_authors
                , author_books):
        """
        initialize all the class attributes.
        """
        self.name = name
        self.author_url = author_url
        self.author_id = author_id
        self.rating = rating
        self.rating_count = rating_count
        self.review_count = review_count
        self.image_url = image_url
        self.related_authors = related_authors
        self.author_books = author_books
    def print_attribute(self):
        """
        print all the attributes.
        """
        print((self.name, self.author_url, self.author_id
        , self.rating, self.rating_count, self.review_count
        , self.image_url,self.related_authors, self.author_books))

    def write_author_to_db(self, cursor):
        """
        write the author attributes to the database.
        Parameters:
                cursor (cursor object of db): The cursor the the db. We can run sql code with this.
        """

        sql_code = """INSERT INTO authors (name, author_url
        , author_id, rating
        , rating_count, review_count
        , image_url, related_authors, author_books) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            cursor.execute(sql_code, self.get_attributes())
        except Exception:
            print("err:unable to send data to the database")

    def get_attributes(self): # return attributes tuple for json parsing
        """"
        return attributes as a tuple
        """

        return (self.name, self.author_url, self.author_id
        , self.rating, self.rating_count, self.review_count
        , self.image_url,self.related_authors, self.author_books)
