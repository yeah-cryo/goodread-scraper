import requests

def test_get_author_success():
    get_obj = requests.get("http://127.0.0.1:5000/api/a", params={'id': '4'}) # requesting with a incorrect url
    assert get_obj.status_code == 404
    assert get_obj.text == "<h1>404</h1><p>The resource could not be found.</p>"