import requests

# API url
url = "http://127.0.0.1:5000/api/scrape"

def test_post_scrape_success():
    post_obj = requests.post(url, params={'attr': 'https://www.goodreads.com/author/show/4.Douglas_Adams'})
    assert post_obj.status_code == 200
    assert post_obj.text == '<h1>POST SUCCESS</h1>'

def test_post_scrape_fail():
    post_obj = requests.post(url, params={'id': 'https://www.goodreads.com/author/show/4.Douglas_Adams'})
    assert post_obj.status_code == 400
    assert post_obj.text == "<h1>400</h1><p>invalid parameter</p>"