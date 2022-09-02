import requests

# API url
url = "http://127.0.0.1:5000/api/author"

def test_put_author_success():
    body = '{"name":"test"}'
    put_obj = requests.put(url,params={'id': '25'}, data =body)
    print(put_obj.text)
    assert put_obj.status_code == 200
    assert put_obj.text == '<h1>PUT SUCCESS</h1>'

def test_put_author_fail_not_json():
    body = "not a json"
    put_obj = requests.put(url,params={'id': '25'}, data =body)
    print(put_obj.text)
    assert put_obj.status_code == 415
    assert put_obj.text == "<h1>415</h1><p>Invalid data Type, requiring JSON</p>"

def test_put_author_fail_invalid_parameter():
    body = '{"name":"test"}'
    put_obj = requests.put(url,params={'attr': '325779'}, data =body)
    assert put_obj.status_code == 400
    assert put_obj.text == "<h1>400</h1><p>invalid parameter</p>"