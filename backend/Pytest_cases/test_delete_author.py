import requests

# API url
url = "http://127.0.0.1:5000/api/author"

def test_delete_author_success():
    delete_obj = requests.delete(url, params={'id': "4"})
    assert delete_obj.status_code == 200
    assert delete_obj.text == '<h1>DELETE SUCCESS</h1>'

def test_delete_author_fail():
    delete_obj = requests.delete(url, params={'attr': "4"})
    assert delete_obj.status_code == 400
    assert delete_obj.text == "<h1>400</h1><p>invalid parameter</p>"