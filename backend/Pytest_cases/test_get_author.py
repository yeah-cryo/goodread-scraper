import requests

# API url
url = "http://127.0.0.1:5000/api/author"

def test_get_author_success():
    get_obj = requests.get(url, params={'id': '4333'})
    assert get_obj.status_code == 200
    dic = get_obj.json()
    print(dic)
    assert dic['authors'][0]['author_id'] == '4333'

def test_get_author_fail():
    get_obj = requests.get(url, params={'attr': '32556779'}) # wrong parameter type
    assert get_obj.status_code == 400
    assert get_obj.text == "<h1>400</h1><p>invalid parameter</p>"