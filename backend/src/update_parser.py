"""the update_parser contains dunctions that convert the primitive query line to sql query line that could update the database"""
from scrape_author_call import *
from scrape_book_call import *
from book import Book
from author import Author

def formater(attribute, value, table, id):
    '''
    The formater formats the command_line of updating a attribute in database.
        Parameters:
                attribute (str): the specific field name.
                value (str): the value to update.
                table (str): table decides which table to update.
                id (str): id determines which row to update.
        Returns:
                command_line (str): the assembled sql command_line for updating a attribute.
    '''
    command_line = ''
    if (table == 'books'):
        command_line = "UPDATE " + table + " SET " + attribute + " = " + "'" + value + "'" + " WHERE book_id = " + id
    if (table == 'authors'):
        command_line = "UPDATE " + table + " SET " + attribute + " = " + "'" +  value + "'"  + " WHERE author_id = " + id
    return command_line

def delete_formatter(id, mycursor, mydb, table):
    '''
    The delete_formatter assembles and runs the command_line of sql delete command.
        Parameters:
                id (str): id determines which row to update.
                mycursor (database cursor object): the cursor used to exceute command line.
                mydb (the database object): mydb is used to commit the change.
                table (str): table decides which table to use.
        Returns:
                (str) the next book url to be scraped.
    '''
    command_line = ''
    if table == 'authors':
        command_line = "DELETE FROM authors WHERE author_id = " + id
    elif table == 'books':
        command_line = "DELETE FROM books WHERE book_id = " + id
    else:
        return 'null'
    try:
        mycursor.execute(command_line)
        mydb.commit()
    except Exception:
        print(command_line)
        return 'null'
    return 'ok'

def scrape_data(url, mydb, mycursor):
    '''
    the scrape_data scrapes one row from the url and post it into the database.
        Parameters:
                url (str): the url to be scraped.
                mycursor (database cursor object): the cursor used to exceute command line.
                mydb (the database object): mydb is used to commit the change.
        Returns:
                (str) the next book url to be scraped.
    '''
    if not ('https://www.goodreads.com/' in url):
        return 'null'
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    try:
        if 'auhtor' in url:
            author_similar_url = get_similar_author(soup)
            cur_author = Author(get_author_name(soup)
            , url, get_author_id(url)
            , get_author_rating(soup)
            , get_author_rating_count(soup)
            , get_author_review_count(soup)
            , get_author_img(soup)
            , author_similar_url, get_list_books(soup))
            cur_author.write_author_to_db(mycursor)
            mydb.commit()
        elif 'book' in url:
            cur_book = Book(url, get_book_title(soup, url)
            ,get_book_id(url), get_book_isbn(soup)
            , get_book_author_url(soup), get_book_author(soup)
            ,  get_book_rating(soup), get_book_rating_counts(soup)
            , get_book_review_count(soup),get_book_img(soup), get_book_similar(soup))
            cur_book.write_book_to_db(mycursor)
            mydb.commit()
    except Exception:
        return 'null'
    return 'DONE'