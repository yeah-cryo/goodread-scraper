import json
from book import Book
from author import Author
from scrape_author_call import *
from scrape_book_call import *
from dic_tuple_converter import *
from query_parser import find_author_by_id, find_book_by_id, querier
from update_parser import formater, scrape_data, delete_formatter

def get_processor(cursor, table, query_line):
    '''
    get_processor simulates the GET api behavior.
        Parameters:
                cursor (database cursor object): the cursor used to exceute command line.
                table (str): table decides which table to update.
                query_line (str): id determines which row to update.
        Returns:
                json.dumps(file_data, indent = 4) (str): the requested json
    '''
    if table == 'book':
        results = find_book_by_id(query_line, cursor)
        if results is None:
            return 'null'
        #convert the results (list of tuple) into json format
        file_data = {'books':[]}
        for cur_tuple in results:
            file_data['books'].append(tuple_to_json_converter_book(cur_tuple))
        return json.dumps(file_data, indent = 4)
    elif table == 'author':
        results = find_author_by_id(query_line, cursor)
        if results is None:
            return 'null'
        #convert the results (list of tuple) into json format
        file_data = {'authors':[]}
        for cur_tuple in results:
            file_data['authors'].append(tuple_to_json_converter_author(cur_tuple))
        return json.dumps(file_data, indent = 4)
    elif table == 'search':
        rt_tp = querier(query_line)
        if rt_tp[0] == 'format_error':
            return 'null'
        command_line = rt_tp[0] + ' ' + rt_tp[1]
        results = []
        try:
            cursor.execute(command_line)
            results = cursor.fetchall()
        except Exception:
            return 'null'
        file_data = {rt_tp[2]:[]}
        for cur_tuple in results:
            if (rt_tp[2] == 'authors'):
                file_data[rt_tp[2]].append(tuple_to_json_converter_author(cur_tuple))
            elif (rt_tp[2] == 'books'):
                file_data[rt_tp[2]].append(tuple_to_json_converter_book(cur_tuple))
        return json.dumps(file_data, indent = 4)

def put_processor(db, cursor, table, query_line, attr, val):
    '''
    put_processor simulates the PUT api behavior.
        Parameters:
                db (the database object): mydb is used to commit the change.
                cursor (database cursor object): the cursor used to exceute command line.
                table (str): table decides which table to update.
                query_line (str): id determines which row to update.
                attr (str): attr determines which field to change.
                val (str): the value to update.
        Returns:
                return 'null' if errors occur.
                return 'DONE' if the requested is complete.
    '''
    dic = {attr:val}
    if len(dic) != 1:
        return 'null'
    key = ''
    attribute = ''
    for ele in dic:
        key = ele
        attribute = dic[ele]
    if table == 'book':
        try:
            cursor.execute(formater(key, attribute, 'books', query_line))
            db.commit()
        except Exception:
            return 'null'
    elif table == 'author':
        try:
            cursor.execute(formater(key, attribute, 'authors', query_line))
            db.commit()
        except Exception:
            return 'null'
    return 'DONE'

def post_query(db, cursor, table,query_line, content):
    '''
    post_processor simulates the POST api behavior.
        Parameters:
                db (the database object): mydb is used to commit the change.
                cursor (database cursor object): the cursor used to exceute command line.
                table (str): table decides which table to update.
                query_line (str): id determines which row to update.
                content (str): the rows that will be added into database.
        Returns:
                return 'null' if errors occur.
                return 'DONE' if the requested is complete.
    '''
    dic = {}
    if table != 'scrape':
        try:
            dic = json.loads(content)
        except Exception:
            return 'null'
    if table == 'book':
        try:
            to_insert = Book(*json_to_tuple_converter_book(dic))
            to_insert.write_book_to_db(cursor)
            db.commit()
        except:
            return 'null'
    elif table == 'books':
        for attributes in dic['content']:
            try:
                to_insert = Book(*json_to_tuple_converter_book(attributes))
                to_insert.write_book_to_db(cursor)
                db.commit()
            except Exception:
                return 'null'
    elif table == 'author':
        try:
            to_insert = Book(*json_to_tuple_converter_author(dic))
            to_insert.write_book_to_db(cursor)
            db.commit()
        except Exception:
            return 'null'
    elif table == 'authors':
        for attributes in dic['content']:
            try:
                to_insert = Book(*json_to_tuple_converter_author(attributes))
                to_insert.write_book_to_db(cursor)
                db.commit()
            except Exception:
                return 'null'
    elif table == 'scrape':
        result = scrape_data(query_line, db, cursor)
        if result == 'null':
            return 'null'
    return 'DONE'

def delete_processor(db, cursor, table, query_line):
    '''
    post_processor simulates the POST api behavior.
        Parameters:
                db (the database object): mydb is used to commit the change.
                cursor (database cursor object): the cursor used to exceute command line.
                table (str): table decides which table to update.
                query_line (str): id determines which row to update.
        Returns:
                return 'null' if errors occur.
                return 'DONE' if the requested is complete.
    '''
    id = query_line
    if table == 'book':
        if delete_formatter(id, cursor, db, 'books') == 'null':
            return 'null'
    elif table == 'author':
        if delete_formatter(id, cursor, db, 'authors') == 'null':
            return 'null'
    return 'DONE'

