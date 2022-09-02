import requests

# API url
url = "http://127.0.0.1:5000/api/search"

def test_get_search_success_book():
    get_obj = requests.get(url, params={'q': 'books.rating: NOT 3 AND books.review_count: > 1234'})
    assert get_obj.status_code == 200

def test_get_search_success_author():
    get_obj = requests.get(url, params={'q': 'authors.rating: NOT 3 AND authors.review_count: > 1234'})
    assert get_obj.status_code == 200

def test_get_search_fail():
    get_obj = requests.get(url, params={'attr': 'books.rating: NOT 3 AND books.review_count: > 1234'})
    assert get_obj.status_code == 400
    assert get_obj.text == "<h1>400</h1><p>invalid parameter</p>"

def test_get_search_invalid_format():
    get_obj = requests.get(url, params={'q': 'books.rating NOT 3'}) # not colon
    assert get_obj.status_code == 400
    assert get_obj.text == "<h1>400</h1><p>invalid parameter</p>"
    get_obj = requests.get(url, params={'q': 'booksrating: NOT 3'}) # not dot
    assert get_obj.status_code == 400
    assert get_obj.text == "<h1>400</h1><p>invalid parameter</p>"