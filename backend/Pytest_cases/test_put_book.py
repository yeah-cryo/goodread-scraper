import requests

# API url
url = "http://127.0.0.1:5000/api/book"

def test_put_book_success():
    body = '{"ISBN":"123456"}'
    put_obj = requests.put(url,params={'id': '325779'}, data =body)
    print(put_obj.text)
    assert put_obj.status_code == 200
    assert put_obj.text == '<h1>PUT SUCCESS</h1>'

def test_put_book_fail_not_json():
    body = "not a json"
    put_obj = requests.put(url,params={'id': '325779'}, data =body)
    print(put_obj.text)
    assert put_obj.status_code == 415
    assert put_obj.text == "<h1>415</h1><p>Invalid data Type, requiring JSON</p>"

def test_put_book_fail_invalid_parameter():
    body = '{"ISBN":"123456"}'
    put_obj = requests.put(url,params={'attr': '325779'}, data =body)
    assert put_obj.status_code == 400
    assert put_obj.text == "<h1>400</h1><p>invalid parameter</p>"