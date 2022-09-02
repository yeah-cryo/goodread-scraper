"""this module contains functions that process raw query line into sql command line"""
def wild_card_field_helper(table, value):
    '''
    helper function of format_checker, wild_card_field_helper assembles the wild sql command line for the query.
        Parameters:
                table (str): the table to query
                value (str): the value of corresponding field.
        Returns:
                query (str): the updated query command line
    '''
    output_query = ''
    if table == 'books':
        output_query = """book_url LIKE %s OR title LIKE %s 
                        OR book_id LIKE %s OR ISBN LIKE %s 
                        OR author_url LIKE %s OR author LIKE %s 
                        OR rating LIKE %s OR rating_count LIKE %s 
                        OR review_count LIKE %s OR image_url LIKE %s 
                        OR similar_books LIKE %s"""
        output_query = output_query%(value, value, value, value
                                    , value, value, value, value
                                    , value, value, value)
    elif table == 'authors':
        output_query =  """name LIKE %s OR author_url LIKE %s OR author_id LIKE %s 
                        OR rating LIKE %s OR rating_count LIKE %s OR review_count LIKE %s
                        OR image_url LIKE %s OR related_authors LIKE %s OR author_books LIKE %s"""
        output_query = output_query%(value, value, value, value
                                    , value, value, value, value
                                    , value)
    # if table is neither books or authors, api route function will return error message
    return output_query 
        
def assembler_helper(query, field, sign, value):
    '''
    helper function of format_checker, assembler_helper assembles the sql command line for the query.
        Parameters:
                sign (str): the equivalence sign includes < > =.
                field (str): the field name of the database.
                value (str): the value of corresponding field.
                content (str): the rows that will be added into database.
        Returns:
                query (str): the updated query command line
                field (str): the field name, it's returned for error checking.
    '''
    try:
        int(value)
    except Exception:
        field = ''
    query = query + 'CAST(' + field + ' AS DECIMAL)' + ' ' + sign + ' ' + value
    return query, field

def format_checker(parse_line):
    '''
    format_checker converts the primitive query line into the sql query command line.
        Parameters:
                parse_line (str): the primitive query line come with the requesting url.
        Returns:
                table (str): the table to be queried
                field (str): the fields that are included in the query condition.
                query (str): the complete condition line of the whole command line.
    '''
    table = ''
    field = ''
    query = ''
    dot_spliter = parse_line.split('.') # split by '.'
    table = dot_spliter[0]
    if len(dot_spliter) > 1:
        colon_spliter = dot_spliter[1].split(':') # split by ':'
        field = colon_spliter[0]
        if len(colon_spliter) > 1:
            temp_query = colon_spliter[1]
            if temp_query[:3] == 'NOT':
                query = query + 'NOT '
                temp_query = temp_query[3:]
            unequal_sign = False
            sign = ''
            if temp_query[0] == '>' or temp_query[0] == '<': # check if < or > exist
                unequal_sign = True
                sign = temp_query[0]
                temp_query = temp_query[1:]
            if temp_query[0] == '"': # check if we have double quote
                value = '"'
                for index,i in enumerate(temp_query[1:]): # iterate through the condition (after : )
                    if i != '"':
                        if index != (len(temp_query[1:]) - 1):
                            if (i == '*'):
                                value = value + '%'
                            else:
                                value = value + i
                    if index == (len(temp_query[1:]) - 1) and i != '"':
                        table = ''
                        field = ''
                value = value + '"'
                if unequal_sign:
                    query, field = assembler_helper(query, field, sign, value) # unequal sign
                elif field == '*':
                    query = wild_card_field_helper(table, value)
                else:
                    query = query + field + ' LIKE ' + value
            else:
                if unequal_sign:
                    query, field = assembler_helper(query, field, sign, temp_query) # unequal sign
                else:
                    query = query + field + ' LIKE ' + '"%' + temp_query + '%"'
    return table, field, query

def querier(arg):
    '''
    querier divide a bigger query line into several small query line by spliting the bigger query line by AND or OR.
    Then querier feed the small query line into format_checker and assembles the results into a more completed query line.
        Parameters:
                arg (str): the Big primitive query line
        Returns:
                select (str): the sql command line prefix that determine which field and table into query.
                condition (str): the conditional sql command line suffix that work as filter of data.
                table_first (str): the table we are querying at.
    '''
    arg = arg.replace(" ", "")
    print(arg)
    args = [arg]
    mid_sign = ''
    if 'AND' in arg:
        args = arg.split('AND')
        mid_sign = 'AND'
    elif 'OR' in arg:
        args = arg.split('OR')
        mid_sign = 'OR'
    select = ''
    condition = "WHERE "
    table_first = ''
    for index,argument in enumerate(args):
        table, field, query = format_checker(argument)
        if (table == '' or field == '' or query == ''):
            return 'format_error', (table , field, query)
        if index == 0:
            table_first = table
            select = "SELECT " + '*' + " FROM " + table
            condition = condition + "(" + query + ")"
            if len(args) == 2:
                condition = condition + ' ' + mid_sign + ' '
        elif index == 1:
            if table != table_first:
                return 'format_error', (table , field, query)
            condition = condition + "(" + query + ")"
            
    return select, condition, table_first

def find_top_n_book(n, cursor):
    q_line = "SELECT title, rating FROM (SELECT title, rating FROM books ORDER BY rating DESC) as tb LIMIT " + n
    try:
        results = []
        cursor.execute(q_line)
        results = cursor.fetchall()
    except Exception:
        return None
    return results

def find_top_n_author(n, cursor):
    q_line = "SELECT name, rating FROM (SELECT name, rating FROM authors ORDER BY rating DESC) as tb LIMIT " + n
    try:
        results = []
        cursor.execute(q_line)
        results = cursor.fetchall()
    except Exception:
        return None
    return results

def find_book_by_id(query_line, cursor):
    '''
    get the sql querying resulting by using the book id.
        Parameters:
                query_line (str): the id that determines which rows to get.
                cursor (database cursor object): the cursor used to exceute command line.
        Returns:
                results (str): the result of the query.
                return None if errors happen while querying.
    '''
    try:
        command_line = "SELECT * FROM books WHERE CAST(book_id AS DECIMAL) = " + query_line
        results = []
        cursor.execute(command_line)
        results = cursor.fetchall()
    except Exception:
        return None
    return results

def find_author_by_id(query_line, cursor):
    '''
    get the sql querying resulting by using the author id.
        Parameters:
                query_line (str): the id that determines which rows to get.
                cursor (database cursor object): the cursor used to exceute command line.
        Returns:
                results (str): the result of the query.
                return None if errors happen while querying.
    '''
    try:
        command_line = "SELECT * FROM authors WHERE CAST(author_id AS DECIMAL) = " + query_line
        results = []
        cursor.execute(command_line)
        results = cursor.fetchall()
    except Exception:
        return None
    return results