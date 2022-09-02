""""this module contains funtions that converts tuple into dictionary or dictionary into tuple"""
def tuple_to_json_converter_book(cur_tuple):
    '''
    convert the book tuple into json format(dictionary).
        Parameters:
                cur_tuple (tuple): the book tuple to be converted into json format.
        Returns:
                dic (disctionary): the json format if the input book tuple.
    '''
    dic = {}
    dic['book_url'] = cur_tuple[0]
    dic['title'] = cur_tuple[1]
    dic['book_id'] = cur_tuple[2]
    dic['ISBN'] = cur_tuple[3]
    dic['author_url'] = cur_tuple[4]
    dic['author'] = cur_tuple[5]
    dic['rating'] = cur_tuple[6]
    dic['rating_count'] = cur_tuple[7]
    dic['review_count'] = cur_tuple[8]
    dic['image_url'] = cur_tuple[9]
    dic['similar_books'] = cur_tuple[10]
    return dic

def tuple_to_dic_special(cur_tuple):
	'''
	convert length 2 tuple to dictionary.
		Parameters:
				cur_tuple (tuple): the tuple to be converted into json format.
		Returns:
				dic (disctionary): the json format if the input tuple.
	'''
	dic = {}
	dic["name"] = cur_tuple[0]
	dic['rating'] = cur_tuple[1]
	return dic

def json_to_tuple_converter_book(dic):
    '''
    convert the book dictionary into tuple.
        Parameters:
                dic (disctionary): the book dictionary to be converted into tuple.
        Returns:
                cur_tuple (tuple): the converted book tuple.
    '''
    t_list = []
    t_list.append(dic['book_url'])
    t_list.append(dic['title'])
    t_list.append(dic['book_id'])
    t_list.append(dic['ISBN'])
    t_list.append(dic['author_url'])
    t_list.append(dic['author'])
    t_list.append(dic['rating'])
    t_list.append(dic['rating_count'])
    t_list.append(dic['review_count'])
    t_list.append(dic['image_url'])
    t_list.append(dic['similar_books'])
    return tuple(t_list)

def tuple_to_json_converter_author(cur_tuple):
    '''
    convert the author tuple into json format(dictionary).
        Parameters:
                cur_tuple (tuple): the author tuple to be converted into json format.
        Returns:
                dic (disctionary): the json format if the input author tuple.
    '''
    dic = {}
    dic['name'] = cur_tuple[0]
    dic['author_url'] = cur_tuple[1]
    dic['author_id'] = cur_tuple[2]
    dic['rating'] = cur_tuple[3]
    dic['rating_count'] = cur_tuple[4]
    dic['review_count'] = cur_tuple[5]
    dic['image_url'] = cur_tuple[6]
    dic['related_authors'] = cur_tuple[7]
    dic['author_books'] = cur_tuple[8]
    return dic

def json_to_tuple_converter_author(dic):
    '''
    convert the author dictionary into tuple.
        Parameters:
                dic (disctionary): the author dictionary to be converted into tuple.
        Returns:
                cur_tuple (tuple): the converted author tuple.
    '''
    t_list = []
    t_list.append(dic['name'])
    t_list.append(dic['author_url'])
    t_list.append(dic['author_id'])
    t_list.append(dic['rating'])
    t_list.append(dic['rating_count'])
    t_list.append(dic['review_count'])
    t_list.append(dic['image_url'])
    t_list.append(dic['related_authors'])
    t_list.append(dic['author_books'])
    return tuple(t_list)