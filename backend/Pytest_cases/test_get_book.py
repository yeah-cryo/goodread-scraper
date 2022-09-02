import requests

# API url
url = "http://127.0.0.1:5000/api/book"

def test_get_book_success():
    get_obj = requests.get(url, params={'id': '325779'})
    assert get_obj.status_code == 200
    dic = get_obj.json()
    assert dic['books'][0]['book_id'] == '325779'

def test_get_book_fail():
    get_obj = requests.get(url, params={'attr': '32556779'}) # wrong parameter type
    assert get_obj.status_code == 400
    assert get_obj.text == "<h1>400</h1><p>invalid parameter</p>"