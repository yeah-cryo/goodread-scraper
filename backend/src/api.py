"""api.py runs the flask apis"""
import flask
import os
import mysql.connector
import sys
import json
sys.path.append('..')
from flask import request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from update_parser import formater, delete_formatter, scrape_data
from src import *
app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True

load_dotenv()
mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('USER'),
  password=os.getenv('PASSWORD'),
  database="goodreadscrape"
)
mycursor = mydb.cursor() # mysql db cursor


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(400)
def invalid_parameter(e):
    return "<h1>400</h1><p>invalid parameter</p>", 400

@app.errorhandler(415)
def invalid_data_type(e):
    return "<h1>415</h1><p>Invalid data Type, requiring JSON</p>", 415

@app.route('/api/book', methods=['GET'])
@cross_origin()
def get_book():
    '''
    get the requested data of book upon requesting by book id.
        Returns:
                (str) The error message(as html) or the requested data
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        return invalid_parameter(400)
    id = query_parameters.get('id')
    results = find_book_by_id(id, mycursor)
    if results is None:
        return invalid_parameter(400)
    file_data = {'books':[]}
    for cur_tuple in results:
        file_data['books'].append(tuple_to_json_converter_book(cur_tuple))
    return json.dumps(file_data, indent = 4)


@app.route('/api/author', methods=['GET'])
@cross_origin()
def get_author():
    '''
    get the requested data of author upon requesting by author id.
        Returns:
                (str) The error message(as html) or the requested data
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        print(len(query_parameters))
        return invalid_parameter(400)
    id = query_parameters.get('id')
    results = find_author_by_id(id, mycursor)
    if results is None:
        return invalid_parameter(400)
    file_data = {'authors':[]}
    for cur_tuple in results:
        file_data['authors'].append(tuple_to_json_converter_author(cur_tuple))
    return json.dumps(file_data, indent = 4)

@app.route('/api/search', methods=['GET'])
@cross_origin()
def get_query():
    '''
    get the requested data of author upon requesting by querying.
        Returns:
                (str) The error message(as html) or the requested data
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        return invalid_parameter(400)
    query = query_parameters.get('q')
    if query is None:
        return invalid_parameter(400)
    rt_tp = querier(query)
    if rt_tp[0] == 'format_error':
        return invalid_parameter(400)
    command_line = rt_tp[0] + ' ' + rt_tp[1]
    print(command_line)
    results = []
    try:
        mycursor.execute(command_line)
        results = mycursor.fetchall()
    except Exception:
        return invalid_parameter(400)
    file_data = {rt_tp[2]:[]}
    for cur_tuple in results:
        if (rt_tp[2] == 'authors'):
            file_data[rt_tp[2]].append(tuple_to_json_converter_author(cur_tuple))
        elif (rt_tp[2] == 'books'):
            file_data[rt_tp[2]].append(tuple_to_json_converter_book(cur_tuple))
    
    return json.dumps(file_data, indent = 4)

@app.route('/api/author', methods=['PUT'])
@cross_origin()
def put_author():
    '''
    update the corresponding data by author id
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    put_in = request.get_data()
    try:
        put_in = put_in.decode("utf-8")
        ans = json.loads(put_in)
    except Exception:
        return invalid_data_type(415)
    query_parameters = request.args
    if len(query_parameters) != 1:
        print(len(query_parameters))
        return invalid_parameter(400)
    id = query_parameters.get('id')
    if len(ans) != 1 or id is None:
        return invalid_parameter(400)
    attribute = ''
    for key in ans:
        attribute = key
    value = ans[attribute]
    print(formater(attribute, value, 'authors', id))
    try:
        mycursor.execute(formater(attribute, value, 'authors', id))
        mydb.commit()
    except Exception:
        return invalid_parameter(400)
    return {"message":'<h1>PUT SUCCESS</h1>'}

@app.route('/api/book', methods=['PUT'])
@cross_origin()
def put_book():
    '''
    update the corresponding data by book id
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    put_in = request.get_data()
    try:
        put_in = put_in.decode("utf-8")
        ans = json.loads(put_in)
    except Exception:
        return invalid_data_type(415)
    query_parameters = request.args
    if len(query_parameters) != 1:
        print(len(query_parameters))
        return invalid_parameter(400)
    id = query_parameters.get('id')
    if len(ans) != 1 or id is None:
        return invalid_parameter(400)
    attribute = ''
    for key in ans:
        attribute = key
    value = ans[attribute]
    
    try:
        mycursor.execute(formater(attribute, value, 'books', id))
        mydb.commit()
    except Exception:
        print(formater(attribute, value, 'books', id))
        return invalid_parameter(400)
    return {"message":'<h1>PUT SUCCESS</h1>'}

@app.route('/api/book', methods=['POST'])
@cross_origin()
def post_book():
    '''
    add one row into the book table
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    put_in = request.get_data()
    try:
        put_in = put_in.decode("utf-8")
        ans = json.loads(put_in)
    except Exception:
        print(put_in)
        return invalid_data_type(415)
    try:
        to_insert = Book(*json_to_tuple_converter_book(ans))
        to_insert.write_book_to_db(mycursor)
        mydb.commit()
    except Exception:
        return invalid_parameter(400)
    return {"message":'<h1>POST SUCCESS</h1>'}

@app.route('/api/books', methods=['POST'])
@cross_origin()
def post_books():
    '''
    add multiple rows into the book table
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    put_in = request.get_data()
    try:
        put_in = put_in.decode("utf-8")
        ans = json.loads(put_in)
    except Exception:
        return invalid_data_type(415)
    try:
        for attributes in ans['content']:
            to_insert = Book(*json_to_tuple_converter_book(attributes))
            to_insert.write_book_to_db(mycursor)
            mydb.commit()
    except Exception:
        return invalid_parameter(400)
    return {"message":'<h1>POST SUCCESS</h1>'}

@app.route('/api/author', methods=['POST'])
@cross_origin()
def post_author():
    '''
    add one row into the author table
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    put_in = request.get_data()
    try:
        put_in = put_in.decode("utf-8")
        ans = json.loads(put_in)
    except Exception:
        return invalid_data_type(415)
    to_insert = Author(*json_to_tuple_converter_author(ans))
    to_insert.write_author_to_db(mycursor)
    mydb.commit()
    try:
        asd = 0
    except Exception:
        return invalid_parameter(400)
    return {"message":'<h1>POST SUCCESS</h1>'}

@app.route('/api/authors', methods=['POST'])
@cross_origin()
def post_authors():
    '''
    add multiple rows into the author table
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    put_in = request.get_data()
    try:
        put_in = put_in.decode("utf-8")
        ans = json.loads(put_in)
    except Exception:
        return invalid_data_type(415)
    try:
        for attributes in ans['content']:
            to_insert = Author(*json_to_tuple_converter_author(attributes))
            to_insert.write_author_to_db(mycursor)
            mydb.commit()
    except Exception:
        return invalid_parameter(400)
    return {"message":'<h1>POST SUCCESS</h1>'}

@app.route('/api/scrape', methods=['POST'])
@cross_origin()
def post_scrape():
    '''
    scrape one row and add it into the book table
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        print(len(query_parameters))
        return invalid_parameter(400)
    url = query_parameters.get('attr')
    if url is None:
        return invalid_parameter(400)
    result = scrape_data(url, mydb, mycursor)
    if result == 'null':
        return invalid_parameter(400)
    return {"message":'<h1>POST SUCCESS</h1>'}

@app.route('/api/author', methods=['DELETE'])
@cross_origin()
def delete_author():
    '''
    delete one row by the author id
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        return invalid_parameter(400)
    id = query_parameters.get('id')
    if id is None:
        return invalid_parameter(400)
    if delete_formatter(id, mycursor, mydb, 'authors') == 'null':
        return invalid_parameter(400)
    return {"message":'<h1>DELETE SUCCESS</h1>'}

@app.route('/api/book', methods=['DELETE'])
@cross_origin()
def delete_book():
    '''
    delete one row by the book id
        Returns:
                (str) The error message(as html) or the succes message(as html)
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        return invalid_parameter(400)
    id = query_parameters.get('id')
    if id is None:
        return invalid_parameter(400)
    if delete_formatter(id, mycursor, mydb, 'books') == 'null':
        print(id)
        return invalid_parameter(400)
    return {"message":'<h1>DELETE SUCCESS</h1>'}

@app.route('/vis/top-books', methods=['GET'])
@cross_origin()
def get_top_n_book():
    '''
    get the requested data of top n book.
        Returns:
                (str) The error message(as html) or the requested data
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        return invalid_parameter(400)
    id = query_parameters.get('id')
    results = find_top_n_book(id, mycursor)
    if results is None:
        return invalid_parameter(400)
    file_data = {'books':[]}
    for cur_tuple in results:
        file_data['books'].append(tuple_to_dic_special(cur_tuple))
    return json.dumps(file_data, indent = 4)

@app.route('/vis/top-authors', methods=['GET'])
@cross_origin()
def get_top_n_author():
    '''
    get the requested data of top n author.
        Returns:
                (str) The error message(as html) or the requested data
    '''
    query_parameters = request.args
    if len(query_parameters) != 1:
        return invalid_parameter(400)
    id = query_parameters.get('id')
    results = find_top_n_author(id, mycursor)
    if results is None:
        return invalid_parameter(400)
    file_data = {'authors':[]}
    for cur_tuple in results:
        file_data['authors'].append(tuple_to_dic_special(cur_tuple))
    print(file_data)
    return json.dumps(file_data, indent = 4)

app.run()

